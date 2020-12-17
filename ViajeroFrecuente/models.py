# Create your models here.
from django.db import models
from _decimal import Decimal
import datetime
from django.conf import settings
from django.utils.timezone import make_aware

class ServiceBase():
    
    def RetrieveAll(self):
        return NULL
    
    def RetrieveById(self, idnum):
        return NULL
    
    def DeleteById(self, idnum):
        return NULL
    
    def Delete(self, entity):
        entity.delete()
        return NULL
    
#     def Create(self, entity):
#         entity.save()     
#         return entity
#     
#     def Update(self, entity):
#         entity.update()      
#         return entity


class ServiceUser(ServiceBase):

    '''USER'''

    def RetrieveAll(self):
        return AppUser.objects.all()
 
    def RetrieveById(self, idnum):
        return AppUser.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        usr = AppUser.objects.get(id=idnum)
        usr.delete()

    def ValidateUserPass(self, user, pwd):
        usr = AppUser.objects.filter(username=user)
        
        if (usr.count() == 0):
            return False
        else:
            newPwd = Utils.hashPassword(self, pwd)
            if (usr.getUsername() == user) and (usr.getPassword() == newPwd):
                return True
            else:
                return False       

#    def Create(self, entity):
#        usrs = AppUser.objects.filter(username=entity.username)
#       if (usrs.count() > 0):
#            raise Exception('User already exists on DB')
#        else:
#            entity.save()     
#            return entity    

class ServiceVehicle(ServiceBase):

    '''VEHICLE'''

    def RetrieveAll(self):
        return Vehicle.objects.all()
 
    def RetrieveById(self, idnum):
        return Vehicle.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        usr = Vehicle.objects.get(id=idnum)
        usr.delete()

#     def Create(self, entity):
#         return entity.Create()
        
#        '''vhcs = Vehicle.objects.filter(licenseplate=entity.licenseplate)'''
#        '''if (vhcs.count() > 0):'''
#        '''   raise Exception('Vehicle already exists on DB')'''
#        '''else:'''
#        '''    entity.save()'''     
#        '''    return entity'''

class ServiceTrip(ServiceBase):

    '''TRIP'''

    def RetrieveAll(self):
        return Trip.objects.all()
 
    def RetrieveById(self, idnum):
        return Trip.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        trip = Trip.objects.get(id=idnum)
        trip.delete()
    
    def Create(self, entity):
        
        qs = Trip.objects.filter(trip_tripstatus=1)         
        qs1 = qs.filter(trip_driver=entity.trip_driver.id)
        qs2 = qs.filter(trip_vehicle=entity.trip_vehicle.id)      
        
        if (qs1.count() > 0):
            raise Exception('Driver is assigned to another trip')

        if (qs2.count() > 0):
            raise Exception('Vehicle is assigned to another trip')
        
        if (entity.trip_passengerqty > entity.trip_vehicle.passengerqty):
            raise Exception('Too many passengers for the selected vehicle')
        else:
            entity.save()     
            return entity
        
class ServiceQualification(ServiceBase):

    '''QUALIFICATION'''

    def RetrieveAll(self):
        return Qualification.objects.all()
 
    def RetrieveById(self, idnum):
        return Qualification.objects.get(id=idnum)
    
    def DeleteById(self, idnum):
        qual = Qualification.objects.get(id=idnum)
        qual.delete()

class Utils():
    
    def encrypt(self, message):
        newS = ''
        for car in message:
            newS = newS + chr(ord(car) + 2)
        return newS
    
    def decrypt(self, message):
        newS = ''
        for car in message:
            newS = newS + chr(ord(car) - 2)
        return newS

    
# Create your models here.
class AppUser(models.Model):
    
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    credits = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    #reputation = Decimal('0.00')
    
    def __str__(self):
        return self.fullname
    
    def getfullName(self):
        return self.fullname

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getCredits(self):
        return self.credits    
    
    #def getReputation(self):
    #    return self.reputation 

    def setfullName(self, fullname):
        self.fullname = fullname

    def setUsername(self, username):
        self.username = username
    
    def setPassword(self, password):
        self.password = Utils.hashPassword(self, password) 
    
    def setCredits(self, creditsToSet):
        self.credits = creditsToSet

    #def setReputation(self, value):
    #    self.reputation = value

    def AddCredits(self, creditsToAdd):
        self.setCredits(self.getCredits() + creditsToAdd)
        self.save()
        return self.getCredits()
    
    def RemoveCredits(self, creditsToRemove):
        self.setCredits(self.getCredits() - creditsToRemove)
        self.save()
        return self.getCredits()
    
    def GetReputation(self):
        '''quals = Qualification.objects.filter(qualification_user__id=user.id)'''
        quals = self.qualification_user.all()
        total = 0
        for qual in quals:
            total = total + qual.qualification_value
        return total / quals.count()
        '''user.setReputation(average)'''
        '''return user'''
   
    def Save(self):
        self.password = Utils().encrypt(self.password) 
        self.save()
        return self
    
class Vehicle(models.Model):
    
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=255)
    licenseplate = models.CharField(max_length=8, unique=True)
    passengerqty = models.IntegerField(default=0)
    drivers = models.ManyToManyField(AppUser)
    
    def getModel(self):
        return self.model    

    def setModel(self, model):
        self.model = model
        
    def getLicensePlate(self):
        return self.licenseplate    

    def setLicensePlate(self, licenseplate):
        self.licenseplate = licenseplate
        
    def getPassengerQty(self):
        return self.passengerqty    

    def setPassengerQty(self, passengerqty):
        self.passengerqty = passengerqty

    def getDrivers(self):
        return self.drivers    

    def setDrivers(self, drivers):
        self.drivers = drivers    
    
    def addDriver(self, driver):
        self.drivers.add(driver)
    
    def removeDriver(self, driver):
        self.drivers.remove(driver)
    
    def __str__(self):
        return self.licenseplate

    def AddDriversToVehicle(self, drivers):
        self.drivers.set(drivers)
        return self

    def Save(self):
        self.save()
        return self

# Create your models here.
class TripStatus(models.Model):
    id = models.AutoField(primary_key=True)
    tripstatus_description = models.CharField(max_length=255)

    def Save(self):
        self.save()
        return self

# Create your models here.
class Trip(models.Model):
    
    id = models.AutoField(primary_key=True)
    trip_date = models.DateTimeField()
    trip_from = models.CharField(max_length=255)
    trip_to = models.CharField(max_length=255)
    trip_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    trip_passengerqty = models.IntegerField(default=0)
    trip_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    trip_driver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='trip_driver')
    trip_passengers = models.ManyToManyField(AppUser, related_name='trip_passengers')
    trip_tripstatus = models.ForeignKey(TripStatus, on_delete=models.CASCADE, related_name='trip_status')

    def setTripStatus(self, tripstatus):
        self.trip_tripstatus = tripstatus
        
    def getTripStatus(self):
        return self.trip_tripstatus

    def setTripDate(self, tripDate):
        self.trip_date = tripDate
        
    def getTripDate(self):
        return self.trip_date

    def setTripFrom(self, tripFrom):
        self.trip_from = tripFrom
        
    def getTripFrom(self):
        return self.trip_from

    def setTripTo(self, tripto):
        self.trip_to = tripto
        
    def getTripTo(self):
        return self.trip_to

    def setAmount(self, amount):
        self.trip_amount = amount
        
    def getAmount(self):
        return self.trip_amount

    def setPassengerQty(self, passengerqty):
        
        ''' AGREGAR VALIDACION AUTO Y CAPACIDAD'''
        self.trip_passengerqty = passengerqty
        
    def getPassengerQty(self):
        return self.trip_passengerqty

    def setVehicle(self, vehicle):
        
        if (self.hasVehicle()):
            self.trip_vehicle.add(vehicle)
        else:
            raise Exception('This trip already has a vehicle')

    def getVehicle(self):
        return self.trip_vehicle
    
    def hasVehicle(self):
        if (self.trip_vehicle.count() == 1):
            return True
        else: 
            return False
        
    def setDriver(self, driver):
        
        if (self.hasDriver()):
            self.trip_driver.add(driver)
        else:
            raise Exception('This trip already has a driver')

    def getDriver(self):
        return self.trip_driver
    
    def hasDriver(self):
        if (self.trip_driver.count() == 1):
            return True
        else: 
            return False
    
    def getPassengers(self):
        return self.trip_passengers
           
    def removePassenger(self, passenger):
        self.trip_passengers.remove(passenger)
                
    def __str__(self):
        return self.tripfrom + ' - ' + self.tripto + ' - ' + self.tripdate

    def hasEmptySpaceLeft(self):
        if (self.getPassengers().count() == self.trip_passengerqty):
            return False
        else:
            return True 
    
    def CloseTrip(self):
        self.trip_tripstatus_id = 2
        self.save()
        return self

    def Save(self):
        
        #NO ESTOY CONVENCIDO DE ESTO
        qs = Trip.objects.filter(trip_tripstatus=1)         
        qs1 = qs.filter(trip_driver=self.trip_driver.id)
        qs2 = qs.filter(trip_vehicle=self.trip_vehicle.id)      
        
        if (qs1.count() > 0):
            raise Exception('Driver is assigned to another trip')

        if (qs2.count() > 0):
            raise Exception('Vehicle is assigned to another trip')
        
        if (self.trip_passengerqty > self.trip_vehicle.passengerqty):
            raise Exception('Too many passengers for the selected vehicle')
        else:
            self.save()     
            return self

    def AddPassengerToTrip(self, passenger):

        if ((self.getAmount() / self.trip_passengerqty) > passenger.getCredits()):
            raise Exception('Not enough credits to pay for this trip')

        if (self.hasEmptySpaceLeft()):
            self.trip_passengers.add(passenger)
            self.save()     
            return self
        else:
            raise Exception('Max Occupancy reached')


class Qualification(models.Model):

    qualification_date = models.DateTimeField()
    qualification_trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    qualification_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='qualification_user')
    qualification_givenby = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='qualification_givenby')
    qualification_value = models.IntegerField(default=0)
    qualification_comments = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    class Meta:
        unique_together = ('qualification_trip', 'qualification_user', 'qualification_givenby')

    def setQualificationDate(self, date):
        self.qualification_date = date
    
    def getQualificationDate(self):
        return self.qualification_date
   
    def setQualificationTrip(self, trip):
        self.qualification_trip = trip
    
    def getQualificationTrip(self):
        return self.qualification_trip
    
    def setQualificationUser(self, user):
        self.qualification_user = user
    
    def getQualificationUser(self):
        return self.qualification_user
    
    def setQualificationGivenBy(self, user):
        self.qualification_givenby = user
    
    def getQualificationGivenBy(self):
        return self.qualification_givenby  
    
    def setQualificationValue(self, value):
        self.qualification_value = value
    
    def getQualificationValue(self):
        return self.qualification_value

    def __str__(self):
        return self.qualification_user + ' - ' + self.qualification_givenby + ' - ' + self.qualification_date

    def Save(self):
        
        date = datetime.datetime.now()      
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        if (self.getQualificationUser().id == self.getQualificationGivenBy().id):
            raise Exception('User giving and receiving feedback is the same')
           
        if (self.getQualificationTrip().getTripDate() > date_with_timezone):
            raise Exception('Incorrect Trip Date')
        else:
            self.save()     
            return self
