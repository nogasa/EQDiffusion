from __future__ import print_function
import pandas as pd
import xlrd
from tabulate import tabulate


class Well():
    '''
    Contains all data for a well.
    '''
    def __init__(self):
        self.API = 0.
        self.api_num = []
        self.district =[]
        self.month =[]
        self.year =[]
        self.yearmonth = []
        self.gross_injection =[]
        self.gross_fluid =[]
        self.water_inj_rate =[]
        self.water_prod_rate =[]
        self.steam_prod_rate =[]
        self.status =[]
        self.type =[]
        self.days =[]
        self.pressure =[]
        self.temperature =[]
        self.density =[]
        self.opcode = []
        self.lease =[]
        self.well_number=[]
        self.TDS =[]
        self.noncondensibles =[]
        self.wellhead =[]
        self.rows = []

    def clear(self):
        '''
        erases contents of the Well_Table
        '''
        self.API = 0.
        self.api_num = []
        self.district =[]
        self.month =[]
        self.year =[]
        self.yearmonth = []
        self.gross_injection =[]
        self.gross_fluid =[]
        self.water_inj_rate =[]
        self.water_prod_rate =[]
        self.steam_prod_rate =[]
        self.status =[]
        self.type =[]
        self.days =[]
        self.pressure =[]
        self.temperature =[]
        self.density =[]
        self.opcode = []
        self.lease =[]
        self.well_number=[]
        self.TDS =[]
        self.noncondensibles =[]
        self.wellhead =[]
        self.rows = []

'''
Takes data from the ./Coso_Well_Logs/DOGGRG_export folder and creates individual text files.
'''

if __name__ == '__main__':

    # Import excel file data using basic python (xlrd)
    api_file = xlrd.open_workbook('./Coso_Well_Logs/Coso_well_log.xls')
    injection_file = xlrd.open_workbook('./Coso_Well_Logs/DOGGRG_export/DOGGRG_Injection.xls')
    steam_file = xlrd.open_workbook('./Coso_Well_Logs/DOGGRG_export/DOGGRG_Steam.xls')
    water_file = xlrd.open_workbook('./Coso_Well_Logs/DOGGRG_export/DOGGRG_Water.xls')
    api_s1 = api_file.sheet_by_index(0)
    injection_s1 = injection_file.sheet_by_index(0)
    steam_s1 = steam_file.sheet_by_index(0)
    water_s1 = water_file.sheet_by_index(0)

    outfolder = './Coso_Well_Logs/Injection_and_Production/'

    # Extract the 'good' API numbers from the API list file, and create a list of them
    api_index_list = api_s1.col_values(0)[1:]
    api0 = api_s1.col_values(2)
    apis = []
    i=1
    for value in api_index_list:
        if value == 'x':
            api_number = api0[i]
            api_number = str(api_number[0:3]+str(api_number[4:]))
            apis.append(int(api_number))
        i=i+1
    # Harvest data from rows with specific API numbers
    for api_number in apis:                     # for each API number/well...
        well = Well()                               # construct an object for the well
        i=1
        for row in injection_s1.col_values(4, start_rowx=1):      # check through all api numbers in the injection sheet
            if str(int(row)) == str(api_number):
                well.opcode.append(injection_s1.cell_value(i, 0))
                well.district.append(injection_s1.cell_value(i,1))
                well.lease.append(injection_s1.cell_value(i, 2))
                well.well_number.append(injection_s1.cell_value(i, 3))
                well.api_num.append(injection_s1.cell_value(i,4))
                well.month.append(injection_s1.cell_value(i, 5))
                well.year.append(str(int(injection_s1.cell_value(i, 6))))
                well.status.append(injection_s1.cell_value(i, 7))
                well.type.append(injection_s1.cell_value(i, 8))
                well.days.append(injection_s1.cell_value(i, 9))
                well.gross_injection.append(injection_s1.cell_value(i, 10))
                well.TDS.append(injection_s1.cell_value(i, 11))
                well.density.append(injection_s1.cell_value(i, 12))
                well.wellhead.append(injection_s1.cell_value(i, 13))
                well.water_inj_rate.append(injection_s1.cell_value(i, 14))
                well.temperature.append(injection_s1.cell_value(i, 15))
                well.pressure.append(injection_s1.cell_value(i, 16))
                well.water_prod_rate.append(0.)
                well.steam_prod_rate.append(0.)
                well.gross_fluid.append(0.)
                # create yearmonth values
                if injection_s1.cell_value(i,5) < 10:
                    month = '0'+str(int(injection_s1.cell_value(i,5)))
                else:
                    month = str(int(injection_s1.cell_value(i,5)))
                well.yearmonth.append(int(str(int(injection_s1.cell_value(i, 6))) + month))
            i=i+1
            j=i
        i=1
        for row in water_s1.col_values(0, start_rowx=1):
            if str(int(row)) == str(api_number):
                well.api_num.append(water_s1.cell_value(i,0))
                well.opcode.append(water_s1.cell_value(i, 1))
                well.lease.append(water_s1.cell_value(i, 2))
                well.well_number.append(water_s1.cell_value(i, 3))
                well.month.append(water_s1.cell_value(i, 4))
                well.year.append(water_s1.cell_value(i, 5))
                well.status.append(water_s1.cell_value(i, 6))
                well.type.append(water_s1.cell_value(i, 7))
                well.days.append(water_s1.cell_value(i, 8))
                well.gross_fluid.append(water_s1.cell_value(i, 9))
                well.TDS.append(water_s1.cell_value(i, 10))
                well.density.append(water_s1.cell_value(i, 12))
                well.wellhead.append(water_s1.cell_value(i, 13))
                well.water_prod_rate.append(water_s1.cell_value(i, 14))
                well.steam_prod_rate.append(water_s1.cell_value(i, 15))
                well.temperature.append(water_s1.cell_value(i, 16))
                well.pressure.append(water_s1.cell_value(i, 17))
                well.district.append(water_s1.cell_value(i, 18))
                well.gross_injection.append(0.)
                well.water_inj_rate.append(0.)
                # create yearmonth values
                if water_s1.cell_value(i, 4) < 10:
                    month = '0' + str(int(water_s1.cell_value(i, 4)))
                else:
                    month = str(int(water_s1.cell_value(i, 4)))
                well.yearmonth.append(int(str(int(water_s1.cell_value(i, 5))) + month))
            i=i+1; j=j+1

        # Iterate through compiled injection & production data arrays and append to well.rows
        i = 0
        for value in well.api_num:
            well.rows.append([well.yearmonth[i], well.opcode[i], well.lease[i], well.well_number[i], well.status[i],
                        well.type[i], well.days[i], well.gross_injection[i], well.water_inj_rate[i], well.gross_fluid[i],
                        well.water_prod_rate[i], well.steam_prod_rate[i], well.TDS[i], well.wellhead[i],
                        well.temperature[i], well.pressure[i], int(well.month[i]), int(well.year[i]), well.api_num[i]])
            i=i+1
        # sort the rows in well.rows
        for i in range(len(well.rows)):
            for j in range(len(well.rows)-1-i):
                if well.rows[j][0] > well.rows[j+1][0]:
                    well.rows[j], well.rows[j+1] = well.rows[j+1], well.rows[j]

        # Write sorted rows to file
        fname = (outfolder + str(api_number)+'.txt')
        file = open(fname, 'w')
        name_row = ' API #   ' + 'opcode ' + '  lease ' + '    well # ' + ' month ' + ' year ' + 'status ' + 'type ' + ' days ' + 'gross_inj ' \
                   + 'water_inj_rate ' + '  gross_fluid  ' + '  water_prod_rate ' + '  steam_prod_rate ' + 'TDS ' + ' wellhead ' + 'temp ' + 'press' + '\n'
        file.write(name_row)

        for row in well.rows:
            # adjust lease string to fit better (too long as of now)
            lease = str(row[2])
            lease = lease[:8]

            string_row = (str(int(row[18])) + '   ' + str(row[1]) + '   ' + lease + '  '+ str(row[3])
                         + '   ' + str(row[16]) +'     '+ str(row[17]) + '  ' + str(row[4]) + '   ' + str(row[5]) + '   '
                         + str(int(row[6])) + '    ' + str(row[7])+ '         ' + str(row[8]) + '          ' + str(row[9])
                         + '             ' + str(row[10]) + '                  ' + str(row[11])+ '     ' + str(row[12]) + '     '
                         + str(row[13]) + '     ' + str(row[14]) + '     ' + str(row[15]))
            file.write(string_row + '\n')
        file.close()
