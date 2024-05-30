from django.db import connection

vehicule_list=[["Combustion engine car", 0.218],["Electric engine car", 0.103], ["Train",0.003, "Bus",0.113]]   
id_vehicule=1
for i in vehicule_list:
        with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_vehicule VALUES (%s,%s,%s)", \
                            [
                                id_vehicule,
                                vehicule_list[i][0],
                                vehicule_list[i][1],
                                
                            ]           
                                       )
        i=i+1