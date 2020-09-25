from django.utils import timezone
from .models import UnPark
import jwt
from ParkingLotSystem import settings
from Users.models import User
from .tasks import send_notification


def un_park(instance):
    ''' 
    function to unpark a vehicle

    Parameters:
    argument(1) instance of type Parking

    Returns:
    deletes vehicle details from parking collection and saves to unparking collection 
    '''
    slot = instance.slot
    vehicle_num = instance.vehicle_num
    entry_time = instance.entry_time
    exit_time = timezone.now()
    charge = calc_charge(exit_time, instance)
    un_parked = UnPark.objects.create(charge=charge,
                                      slot=slot,
                                      entry_time=entry_time,
                                      exit_time=exit_time,
                                      vehicle_num=vehicle_num)
    un_parked.save()
    instance.delete()


def calc_charge(exit_time, instance):
    ''' 
    function that calculates charge

    Parameters:
    argument(1) exit time
    argument(2) instance of type parking

    Returns:
    total charge based on role,park and vehicle type
    '''
    total_parked_time = (exit_time - instance.entry_time)
    total_hours = total_parked_time.total_seconds() / 3600
    if total_hours < 1:
        total_hours = 1
    charges = total_hours * (float(instance.vehicle_type.charge) + float(
        instance.park_type.charge) + float(instance.user.role.charge))
    if instance.disabled:
        DISCOUNT = 0.1
        charges = charges - (charges * DISCOUNT)
    return charges


def assign_slot(slots_taken):
    ''' 
    function that assigns slot for parking vehicle

    Parameters:
    argument(1) a set containing the values of slots that are taken

    Returns:
    total charge based on role,park and vehicle type
    '''
    total_slots = set(range(1, 401))
    slot = list(total_slots.difference(slots_taken))
    if len(slot) < 1:
        send_email()
        return 0
    return slot[0]


def send_email():
    user_details = User.objects.all()
    for user in user_details:
        print(user.role)
        if user.role == "security" or user.role == "police":
            send_notification.delay(user.email, user.username)
            return 0
