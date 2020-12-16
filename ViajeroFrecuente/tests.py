import datetime
from django.test import TestCase
from ViajeroFrecuente.models import AppUser, Utils, Qualification, Trip, Vehicle, ServiceUser, ServiceVehicle, TripStatus
from _decimal import Decimal
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import timedelta

# Create your tests here.
class AppUserModelTests(TestCase):

    def test_was_created_successfully(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 300
        
        usr = usr.Save()
        
        savedUsr = ServiceUser().RetrieveById(usr.id)

        self.assertIsNotNone(savedUsr)
 
    def test_credits_were_assigned_ok(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr = usr.Save()
        savedUsr = ServiceUser().RetrieveById(usr.id)
         
        self.assertEqual(savedUsr.getCredits(), Decimal('400.00'))
         
    def test_credits_were_added_ok(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        savedUsr = usr.Save()

        savedUsr = ServiceUser().RetrieveById(savedUsr.id)
        
        newCredits = savedUsr.AddCredits(100)  
         
        self.assertEqual(newCredits, Decimal('500.00'))
 
    def test_credits_were_removed_ok(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr = usr.Save()
        savedUsr = ServiceUser().RetrieveById(usr.id)
        
        newCredits = savedUsr.RemoveCredits(100)  
         
        self.assertEqual(newCredits, Decimal('300.00'))
 
    def test_validate_user_and_pass(self):

        usr = AppUser()
        originalPwd = 'pwd1'
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = originalPwd
        usr.credits = 400
         
        usr.Save()
         
        savedUsr = ServiceUser().RetrieveAll().first()

        self.assertEqual(savedUsr.getUsername(), usr.username)         
        self.assertEqual(savedUsr.getPassword(), Utils().encrypt(originalPwd))
         
    def test_validate_get_reputation_result(self):

        usr1 = AppUser()
        usr1.fullname = 'TEST NOMBRE COMPLETO'
        usr1.username = 'TEST1'
        usr1.password = 'pwd1'
        usr1.credits = 400

        usr2 = AppUser()
        usr2.fullname = 'TEST NOMBRE COMPLETO'
        usr2.username = 'TEST2'
        usr2.password = 'pwd1'
        usr2.credits = 400
        
        usr3 = AppUser()
        usr3.fullname = 'TEST NOMBRE COMPLETO'
        usr3.username = 'TEST3'
        usr3.password = 'pwd1'
        usr3.credits = 400        
            
        usr1 = usr1.Save()      
        usr2 = usr2.Save()
        usr3 = usr3.Save() 
             
        usrCol = [usr1]
          
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVE"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 1000
        trip.trip_driver = usr1
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
         
        trip = trip.Save()
        
        tripStatus2 = TripStatus()
        tripStatus2.tripstatus_description = "CLOSED"
        tripStatus2 = tripStatus2.Save()
        trip = trip.CloseTrip()
 
        '''CREATE TRIP'''
        trip2 = Trip()
        trip2.trip_date = date_with_timezone
        trip2.trip_amount = 1000
        trip2.trip_driver = usr1
        trip2.trip_from = 'ORIGEN'
        trip2.trip_to = 'DESTINO'
        trip2.trip_passengerqty = 5
        trip2.trip_vehicle = vehicle
        trip2.trip_tripstatus = tripStatus2
    
        trip2 = trip2.Save()
         
        qual = Qualification()
        qual.qualification_date = date_with_timezone
        qual.qualification_givenby = usr2
        qual.qualification_user = usr1
        qual.qualification_trip = trip
        qual.qualification_value = 5
         
        qual = qual.Save()
         
        qual = Qualification()
        qual.qualification_date = date_with_timezone
        qual.qualification_givenby = usr3
        qual.qualification_user = usr1
        qual.qualification_trip = trip2
        qual.qualification_value = 4
         
        qual = qual.Save()
        
        reputation = usr1.GetReputation()
        
        '''qualUser = ServiceUser.GetReputationByUser(self, savedUsr)'''
         
        self.assertEqual(reputation, Decimal('4.5'))

    def test_create_two_users_with_same_login(self):
        
        usr = AppUser()
        usr.setfullName('TEST NOMBRE COMPLETO')
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr = usr.Save()
        
        usr2 = AppUser()
        usr2.setfullName('TEST NOMBRE COMPLETO')
        usr2.username = 'TEST1'
        usr2.password = 'pwd1'
        usr2.credits = 400
         
        with self.assertRaises(Exception) as context:
            usr2.Save()

        self.assertEqual('UNIQUE constraint failed: ViajeroFrecuente_appuser.username', context.exception.args[0]) 

class VehicleModelTests(TestCase):

    def test_was_created_successfully(self):

        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        savedVehicle = ServiceVehicle().RetrieveById(vehicle.id)

        self.assertIsNotNone(savedVehicle)
        
    def test_were_drivers_added_successfully_to_vehicle(self):

        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        savedVehicle = ServiceVehicle().RetrieveById(vehicle.id)
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO1'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr = usr.Save()
        savedUsr1 = ServiceUser().RetrieveById(usr.id)

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO2'
        usr.username = 'TEST2'
        usr.password = 'pwd2'
        usr.credits = 400
         
        usr = usr.Save()
        savedUsr2 = ServiceUser().RetrieveById(usr.id)
         
        usrCol = [savedUsr1, savedUsr2]

        savedVehicle.AddDriversToVehicle(usrCol)

        self.assertEqual(vehicle.drivers.count(), 2)  

    def test_create_two_vehicles_with_same_licenseplate(self):
        
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle2 = Vehicle()
        vehicle2.model = 'FORD FOCUS'
        vehicle2.licenseplate = 'ABC123'
        vehicle2.passengerqty = 5
         
        with self.assertRaises(Exception) as context:
            vehicle2 = vehicle2.Save()

        self.assertEqual('UNIQUE constraint failed: ViajeroFrecuente_vehicle.licenseplate', context.exception.args[0]) 

class TripModelTests(TestCase):

    def test_was_created_successfully(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 1000
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
         
         
        savedTrip = trip.Save()

        self.assertIsNotNone(savedTrip)

    def test_trip_has_more_passengers_than_vehicle(self):
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()  
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 1000
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 6
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
         
        with self.assertRaises(Exception) as context:
            trip.Save()
            
        self.assertEqual('Too many passengers for the selected vehicle', context.exception.args[0]) 

    def test_trip_has_no_available_space(self):
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 200
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
        
        savedTrip = trip.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr1 = usr.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO2'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr2 = usr.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO3'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr3 = usr.Save()
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO4'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr4 = usr.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO5'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr5 = usr.Save()
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO6'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr6 = usr.Save()

        savedTrip.AddPassengerToTrip(usr1)
        savedTrip.AddPassengerToTrip(usr2)
        savedTrip.AddPassengerToTrip(usr3)
        savedTrip.AddPassengerToTrip(usr4)
        savedTrip.AddPassengerToTrip(usr5)

        with self.assertRaises(Exception) as context:
            savedTrip.AddPassengerToTrip(usr6)
            
        self.assertEqual('Max Occupancy reached', context.exception.args[0]) 

    def test_passenger_has_no_enough_credits_to_pay_trip(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 400
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
        
        savedTrip = trip.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO1'
        usr.password = 'pwd1'
        usr.credits = 50
         
        usr = usr.Save()

        with self.assertRaises(Exception) as context:
            savedTrip.AddPassengerToTrip(usr)
            
        self.assertEqual('Not enough credits to pay for this trip', context.exception.args[0]) 

    def test_trip_driver_has_another_active_trip(self):

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle2 = Vehicle()
        vehicle2.model = 'FORD FOCUS'
        vehicle2.licenseplate = 'ABC124'
        vehicle2.passengerqty = 5
        
        vehicle2 = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 1000
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
         
        trip.Save()

        '''CREATE TRIP'''
        trip2 = Trip()
        trip2.trip_date = date_with_timezone
        trip2.trip_amount = 1000
        trip2.trip_driver = savedUsr
        trip2.trip_from = 'ORIGEN'
        trip2.trip_to = 'DESTINO'
        trip2.trip_passengerqty = 5
        trip2.trip_vehicle = vehicle2
        trip2.trip_tripstatus = tripStatus         

        with self.assertRaises(Exception) as context:
            trip2.Save()
            
        self.assertEqual('Driver is assigned to another trip', context.exception.args[0]) 

    def test_trip_vehicle_has_another_active_trip(self):

        '''USUARIO 1'''
        usr1 = AppUser()
        usr1.fullname = 'TEST NOMBRE COMPLETO'
        usr1.username = 'TEST1'
        usr1.password = 'pwd1'
        usr1.credits = 400         
        usr1 = usr1.Save()

        '''USUARIO 2'''
        usr2 = AppUser()
        usr2.fullname = 'TEST NOMBRE COMPLETO'
        usr2.username = 'TEST2'
        usr2.password = 'pwd1'
        usr2.credits = 400
        usr2.Save()
         
        '''CREATE 1 VEHICLE'''   
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
        
        vehicle.drivers.set([usr1])
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
         
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save() 
         
        '''CREATE TRIP 1'''
        trip1 = Trip()
        trip1.trip_date = date_with_timezone
        trip1.trip_amount = 1000
        trip1.trip_driver = usr1
        trip1.trip_from = 'ORIGEN'
        trip1.trip_to = 'DESTINO'
        trip1.trip_passengerqty = 5
        trip1.trip_vehicle = vehicle
        trip1.trip_tripstatus = tripStatus
         
        trip1 = trip1.Save()

        '''CREATE TRIP 2'''
        trip2 = Trip()
        trip2.trip_date = date_with_timezone
        trip2.trip_amount = 1000
        trip2.trip_driver = usr2
        trip2.trip_from = 'ORIGEN'
        trip2.trip_to = 'DESTINO'
        trip2.trip_passengerqty = 5
        trip2.trip_vehicle = vehicle
        trip2.trip_tripstatus = tripStatus         

        with self.assertRaises(Exception) as context:
            trip2 = trip2.Save()
            
        self.assertEqual('Vehicle is assigned to another trip', context.exception.args[0]) 

class QualificationModelTests(TestCase):

    def test_was_created_successfully(self):
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = 'pwd1'
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 200
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
        
        savedTrip = trip.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO1'
        usr.password = Utils.encrypt(self, 'pwd1')
        usr.credits = 400

        psngr = usr.Save()
        
        savedTrip = savedTrip.AddPassengerToTrip(psngr)

        date = datetime.datetime.now()        
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(psngr)
        qual.setQualificationValue(5)
        
        savedQual = qual.Save()

        self.assertIsNotNone(savedQual)

    def test_qualification_has_a_future_date(self):
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = Utils.encrypt(self, 'pwd1')
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now() + timedelta(days=1)       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 200
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
        
        savedTrip = trip.Save()

        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'PASAJERO1'
        usr.password = Utils.encrypt(self, 'pwd1')
        usr.credits = 400

        psngr = usr.Save()
        
        savedTrip = savedTrip.AddPassengerToTrip(psngr)

        date = datetime.datetime.now()       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(psngr)
        qual.setQualificationValue(5)
        
        with self.assertRaises(Exception) as context:
            qual.Save()
            
        self.assertEqual('Incorrect Trip Date', context.exception.args[0])       

    def test_qualification_is_given_by_same_user(self):
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST1'
        usr.password = Utils.encrypt(self, 'pwd1')
        usr.credits = 400
         
        usr.Save()
        savedUsr = ServiceUser().RetrieveAll().first()
         
        usrCol = [savedUsr]
         
        '''CREATE VEHICLE'''
          
        vehicle = Vehicle()
        vehicle.model = 'FORD FOCUS'
        vehicle.licenseplate = 'ABC123'
        vehicle.passengerqty = 5
        
        vehicle = vehicle.Save()
         
        vehicle.drivers.set(usrCol)
                  
        date = datetime.datetime.now() + timedelta(days=1)       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)
        
        '''CREATE TRIP STATUS'''
        tripStatus = TripStatus()
        tripStatus.tripstatus_description = "ACTIVO"
        tripStatus = tripStatus.Save()
         
        '''CREATE TRIP'''
        trip = Trip()
        trip.trip_date = date_with_timezone
        trip.trip_amount = 200
        trip.trip_driver = savedUsr
        trip.trip_from = 'ORIGEN'
        trip.trip_to = 'DESTINO'
        trip.trip_passengerqty = 5
        trip.trip_vehicle = vehicle
        trip.trip_tripstatus = tripStatus
        
        savedTrip = trip.Save()
        
        usr = AppUser()
        usr.fullname = 'TEST NOMBRE COMPLETO'
        usr.username = 'TEST2'
        usr.password = Utils.encrypt(self, 'pwd1')
        usr.credits = 400
         
        psngr = usr.Save()
                
        savedTrip = savedTrip.AddPassengerToTrip(psngr)

        date = datetime.datetime.now()       
        settings.TIME_ZONE  # 'UTC'
        date_with_timezone = make_aware(date)

        qual = Qualification()
        qual.setQualificationDate(date_with_timezone)
        qual.setQualificationTrip(savedTrip)
        qual.setQualificationUser(savedUsr)
        qual.setQualificationGivenBy(savedUsr)
        qual.setQualificationValue(5)
        
        with self.assertRaises(Exception) as context:
            qual.Save()
            
        self.assertEqual('User giving and receiving feedback is the same', context.exception.args[0])                       

class UtilsTests(TestCase):
    
        def test_is_encryption_working(self):
            
            text = "AHI VIENE LA PRUEBA!"
            cryptText = Utils.encrypt(self, text)
            self.assertEqual(text, Utils.decrypt(self, cryptText))
