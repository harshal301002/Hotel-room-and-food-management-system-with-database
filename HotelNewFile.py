import time
from tkinter import *
from tkcalendar import Calendar, DateEntry
from datetime import date
import datetime
import random
import cx_Oracle
import math

#----------------------------------------------Creating Main Window----------------------------------------------------
root = Tk()
root.geometry('1500x750')
root.configure(bg='#f2f3d2')

#-----------------------------------------------Functions for Main Frame Buttons---------------------------------------

#Functions for Button Functioning


def insert_op_cust(name, phone_num, num_beds, room_num, check_in):
    sql = 'insert into customer (name, phone_number, beds, room_num, check_in) values(:name, :phone_num, :num_beds, :room_num, :check_in)'
    check_in = datetime.datetime.strptime(check_in, "%m/%d/%y")
    check_in = check_in.strftime("%d-%b-%y")
    print(check_in)

    try:
        with cx_Oracle.connect(user="demopython",
                               password="himanshu",
                               dsn="localhost/xepdb1") as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, [name, phone_num, num_beds, room_num, check_in])

                connection.commit()
    except cx_Oracle.Error as error:
        print('Error Occured:')
        print(error)
    else:
        print("Value Inserted")


def select_op():
    sql = 'SELECT * FROM customer'

    try:
        with cx_Oracle.connect(user="demopython",
                               password="himanshu",
                               dsn="localhost/xepdb1") as connection:
            with connection.cursor() as cursor:
                x = cursor.execute(sql)

                data = x.fetchall()

        return data

    except cx_Oracle.Error as error:
        print('Error Occured:')
        print(error)


def update_op(sel_name, sel_number, checkout):
    # sql = 'UPDATE customer SET Check_out = :check_out WHERE Name = :name AND Phone_Number = :number'
    #
    # try:
    #     with cx_Oracle.connect(user="demopython",
    #                            password="himanshu",
    #                            dsn="localhost/xepdb1") as connection:
    #
    #         with connection.cursor() as cursor:
    #             print("Here 3")
    #             cursor.execute(sql, [name, number, check_out])
    #             print("Here 4")
    #
    # except cx_Oracle.Error as error:
    #     print('Error Occured:')
    #     print(error)
    # else:
    #     print("Value Updated")

    sql = "update customer set Check_out=:Check_out where Name=:Name and Phone_Number=:Phone_Number"

    try:
        with cx_Oracle.connect(user="demopython",
                               password="himanshu",
                               dsn="localhost/xepdb1") as connection:

            with connection.cursor() as cursor:
                cursor.execute(sql, (checkout, sel_name, sel_number))
                connection.commit()

    except cx_Oracle.Error as error:
        print(error)


def def_main_page():
    def allocate_room():
        x = clicked_bed.get()
        global room

        try:
            if x == bed_option[0]:
                room_num = random.choice(single_bed_available_rooms)
                single_bed_occupied.append(single_bed_available_rooms.pop(single_bed_available_rooms.index(room_num)))
            elif x == bed_option[1]:
                room_num = random.choice(double_bed_available_rooms)
                double_bed_occupied.append(double_bed_available_rooms.pop(double_bed_available_rooms.index(room_num)))
            else:
                room_num = random.choice(triple_bed_available_rooms)
                triple_bed_occupied.append(triple_bed_available_rooms.pop(triple_bed_available_rooms.index(room_num)))
        except IndexError:
            Label(main_frame, text='None', font=('Helvatical Bold', 11)).grid(row=3, column=1, padx=5, pady=5)
            room = 'None'
        else:
            Label(main_frame, text=room_num).grid(row=3, column=1, padx=5, pady=5)
            room = room_num

        #DATABASE CONNECTION FOR INSERTING DATA
        if room != 'None':
            insert_op_cust(name_entry.get(),
                      int(phone_num_entry.get()),
                      int(clicked_bed.get()[0]),
                      int(room),
                      check_in_entry.get_date())

    #For Number of Beds DropDown
    bed_option = ['1 Bed(800)',
                  '2 Bed(1500)',
                  '3 Bed(2000)']
    clicked_bed = StringVar()
    clicked_bed.set('1 Bed(800)')

    #For Check in Date
    today_date = date.today()

    #Labels for entry boxes
    name_label = Label(main_frame, text='NAME:', font=('Helvatical Bold', 11), bg='#f2f3d2')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    phone_num_label = Label(main_frame, text='PHONE NUMBER:', font=('Helvatical Bold', 11), bg='#f2f3d2')
    phone_num_label.grid(row=1, column=0, padx=5, pady=5)
    num_beds_label = Label(main_frame, text='NUMBER OF BEDS:', font=('Helvatical Bold', 11), bg='#f2f3d2')
    num_beds_label.grid(row=2, column=0, padx=5, pady=5)
    room_num_label = Label(main_frame, text='ROOM NUMBER:', font=('Helvatical Bold', 11), bg='#f2f3d2')
    room_num_label.grid(row=3, column=0, padx=5, pady=5)
    check_in_label = Label(main_frame, text='CHECK IN DATE:', font=('Helvatical Bold', 11), bg='#f2f3d2')
    check_in_label.grid(row=4, column=0, padx=5, pady=5)

    name_entry = Entry(main_frame, width=10, bd=3, relief=SUNKEN, font=('Helvatical Bold', 11))
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    phone_num_entry = Entry(main_frame, width=10, bd=3, relief=SUNKEN, font=('Helvatical Bold', 11))
    phone_num_entry.grid(row=1, column=1, padx=5, pady=5)
    num_beds_entry = OptionMenu(main_frame, clicked_bed, *bed_option)
    num_beds_entry.grid(row=2, column=1, padx=5, pady=5)
    check_in_entry = Calendar(main_frame, selectmode='day', year=today_date.year, month=today_date.month, day=today_date.day)
    check_in_entry.grid(row=4, column=1, padx=5, pady=5)

    room_button = Button(main_frame, text='Allocate Room', bd=5, relief=RIDGE, command=allocate_room, font=('Helvatical Bold', 11))
    room_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


def def_food_facility():
    #variables
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    var7 = IntVar()
    var8 = IntVar()

    var9 = IntVar()
    var10 = IntVar()
    var11 = IntVar()
    var12 = IntVar()
    var13 = IntVar()
    var14 = IntVar()
    var15 = IntVar()
    var16 = IntVar()

    var17 = IntVar()
    var18 = IntVar()
    var19 = IntVar()
    var20 = IntVar()
    var21 = IntVar()
    var22 = IntVar()
    var23 = IntVar()
    var24 = IntVar()

    var25 = IntVar()
    var26 = IntVar()
    var27 = IntVar()
    var28 = IntVar()
    var29 = IntVar()
    var30 = IntVar()
    var31 = IntVar()
    var32 = IntVar()

    DateofOrder = StringVar()
    SubTotal = StringVar()
    Paid_Tax = StringVar()
    Total_Cost = StringVar()
    Servicecharge = StringVar()
    Costofdrinks = StringVar()
    Costofstarters = StringVar()
    Costofmain = StringVar()
    Costofdessert = StringVar()

    E_coke = StringVar()
    E_pepsi = StringVar()
    E_sprite = StringVar()
    E_milkshake = StringVar()
    E_tea = StringVar()
    E_coffee = StringVar()
    E_cold_coffee = StringVar()
    E_beer = StringVar()

    E_manchow = StringVar()
    E_tomato = StringVar()
    E_manchurian = StringVar()
    E_fries = StringVar()
    E_noodles = StringVar()
    E_paneerchilly = StringVar()
    E_redpasta = StringVar()
    E_whitepasta = StringVar()

    E_paneer_tikka = StringVar()
    E_paneer_butter = StringVar()
    E_butter_roti = StringVar()
    E_roti = StringVar()
    E_chana = StringVar()
    E_mixveg = StringVar()
    E_paratha = StringVar()
    E_laccha = StringVar()

    E_chocolate = StringVar()
    E_strawberry = StringVar()
    E_pineapple = StringVar()
    E_brownie = StringVar()
    E_chocochips = StringVar()
    E_vanilla = StringVar()
    E_blackforest = StringVar()
    E_whiteforest = StringVar()

    E_coke.set("0")
    E_pepsi.set("0")
    E_sprite.set("0")
    E_milkshake.set("0")
    E_tea.set("0")
    E_coffee.set("0")
    E_cold_coffee.set("0")
    E_beer.set("0")

    E_manchow.set("0")
    E_tomato.set("0")
    E_manchurian.set("0")
    E_fries.set("0")
    E_noodles.set("0")
    E_paneerchilly.set("0")
    E_redpasta.set("0")
    E_whitepasta.set("0")

    E_paneer_tikka.set("0")
    E_paneer_butter.set("0")
    E_butter_roti.set("0")
    E_roti.set("0")
    E_chana.set("0")
    E_mixveg.set("0")
    E_paratha.set("0")
    E_laccha.set("0")

    E_chocolate.set("0")
    E_strawberry.set("0")
    E_pineapple.set("0")
    E_brownie.set("0")
    E_chocochips.set("0")
    E_vanilla.set("0")
    E_blackforest.set("0")
    E_whiteforest.set("0")

    curdate = datetime.datetime.today()
    DateofOrder.set(curdate.strftime("%A,%d/%m/%Y,%H:%M:%S"))

    #Functions for Enabling TextBoxes
    def chk_coke():
        if var1.get() == 1:
            coke_entry.configure(state=NORMAL)
            coke_entry.focus()
            coke_entry.delete('0', END)
            E_coke.set("")
        elif var1.get() == 0:
            coke_entry.configure(state=DISABLED)
            E_coke.set("0")

    def chk_pepsi():
        if var2.get() == 1:
            pepsi_entry.configure(state=NORMAL)
            pepsi_entry.focus()
            pepsi_entry.delete('0', END)
            E_pepsi.set("")
        elif var2.get() == 0:
            pepsi_entry.configure(state=DISABLED)
            E_pepsi.set("0")

    def chk_sprite():
        if var3.get() == 1:
            sprite_entry.configure(state=NORMAL)
            sprite_entry.focus()
            sprite_entry.delete('0', END)
            E_sprite.set("")
        elif var3.get() == 0:
            sprite_entry.configure(state=DISABLED)
            E_sprite.set("0")

    def chk_milkshake():
        if var4.get() == 1:
            milkshake_entry.configure(state=NORMAL)
            milkshake_entry.focus()
            milkshake_entry.delete('0', END)
            E_milkshake.set("")
        elif var4.get() == 0:
            milkshake_entry.configure(state=DISABLED)
            E_milkshake.set("0")

    def chk_tea():
        if var5.get() == 1:
            tea_entry.configure(state=NORMAL)
            tea_entry.focus()
            tea_entry.delete('0', END)
            E_tea.set("")
        elif var5.get() == 0:
            tea_entry.configure(state=DISABLED)
            E_tea.set("0")

    def chk_coffee():
        if var6.get() == 1:
            coffee_entry.configure(state=NORMAL)
            coffee_entry.focus()
            coffee_entry.delete('0', END)
            E_coffee.set("")
        elif var6.get() == 0:
            coffee_entry.configure(state=DISABLED)
            E_coffee.set("0")

    def chk_cold_coffee():
        if var7.get() == 1:
            cold_coffee_entry.configure(state=NORMAL)
            cold_coffee_entry.focus()
            cold_coffee_entry.delete('0', END)
            E_cold_coffee.set("")
        elif var7.get() == 0:
            cold_coffee_entry.configure(state=DISABLED)
            E_cold_coffee.set("0")

    def chk_beer():
        if var8.get() == 1:
            beer_entry.configure(state=NORMAL)
            beer_entry.focus()
            beer_entry.delete('0', END)
            E_beer.set("")
        elif var8.get() == 0:
            beer_entry.configure(state=DISABLED)
            E_beer.set("0")

    def chk_manchow():
        if var9.get() == 1:
            manchow_entry.configure(state=NORMAL)
            manchow_entry.focus()
            manchow_entry.delete('0', END)
            E_manchow.set("")
        elif var9.get() == 0:
            manchow_entry.configure(state=DISABLED)
            E_manchow.set("0")

    def chk_tomato():
        if var10.get() == 1:
            tomato_entry.configure(state=NORMAL)
            tomato_entry.focus()
            tomato_entry.delete('0', END)
            E_tomato.set("")
        elif var10.get() == 0:
            tomato_entry.configure(state=DISABLED)
            E_tomato.set("0")

    def chk_manchurian():
        if var11.get() == 1:
            manchurian_entry.configure(state=NORMAL)
            manchurian_entry.focus()
            manchurian_entry.delete('0', END)
            E_manchurian.set("")
        elif var11.get() == 0:
            manchurian_entry.configure(state=DISABLED)
            E_manchurian.set("0")

    def chk_fries():
        if var12.get() == 1:
            fries_entry.configure(state=NORMAL)
            fries_entry.focus()
            fries_entry.delete('0', END)
            E_fries.set("")
        elif var12.get() == 0:
            fries_entry.configure(state=DISABLED)
            E_fries.set("0")

    def chk_noodles():
        if var13.get() == 1:
            noodles_entry.configure(state=NORMAL)
            noodles_entry.focus()
            noodles_entry.delete('0', END)
            E_noodles.set("")
        elif var13.get() == 0:
            noodles_entry.configure(state=DISABLED)
            E_noodles.set("0")

    def chk_paneerchilly():
        if var14.get() == 1:
            paneerchilly_entry.configure(state=NORMAL)
            paneerchilly_entry.focus()
            paneerchilly_entry.delete('0', END)
            E_paneerchilly.set("")
        elif var14.get() == 0:
            paneerchilly_entry.configure(state=DISABLED)
            E_paneerchilly.set("0")

    def chk_redpasta():
        if var15.get() == 1:
            redpasta_entry.configure(state=NORMAL)
            redpasta_entry.focus()
            redpasta_entry.delete('0', END)
            E_redpasta.set("")
        elif var15.get() == 0:
            redpasta_entry.configure(state=DISABLED)
            E_redpasta.set("0")

    def chk_whitepasta():
        if var16.get() == 1:
            whitepasta_entry.configure(state=NORMAL)
            whitepasta_entry.focus()
            whitepasta_entry.delete('0', END)
            E_whitepasta.set("")
        elif var16.get() == 0:
            whitepasta_entry.configure(state=DISABLED)
            E_whitepasta.set("0")

    def chk_paneer_tikka():
        if var17.get() == 1:
            paneer_tikka_entry.configure(state=NORMAL)
            paneer_tikka_entry.focus()
            paneer_tikka_entry.delete('0', END)
            E_paneer_tikka.set("")
        elif var17.get() == 0:
            paneer_tikka_entry.configure(state=DISABLED)
            E_paneer_tikka.set("0")

    def chk_paneer_butter():
        if var18.get() == 1:
            paneer_butter_entry.configure(state=NORMAL)
            paneer_butter_entry.focus()
            paneer_butter_entry.delete('0', END)
            E_paneer_butter.set("")
        elif var18.get() == 0:
            paneer_butter_entry.configure(state=DISABLED)
            E_paneer_butter.set("0")

    def chk_butter_roti():
        if var19.get() == 1:
            butter_roti_entry.configure(state=NORMAL)
            butter_roti_entry.focus()
            butter_roti_entry.delete('0', END)
            E_butter_roti.set("")
        elif var19.get() == 0:
            butter_roti_entry.configure(state=DISABLED)
            E_butter_roti.set("0")

    def chk_roti():
        if var20.get() == 1:
            roti_entry.configure(state=NORMAL)
            roti_entry.focus()
            roti_entry.delete('0', END)
            E_roti.set("")
        elif var20.get() == 0:
            roti_entry.configure(state=DISABLED)
            E_roti.set("0")

    def chk_chana():
        if var21.get() == 1:
            chana_entry.configure(state=NORMAL)
            chana_entry.focus()
            chana_entry.delete('0', END)
            E_chana.set("")
        elif var21.get() == 0:
            chana_entry.configure(state=DISABLED)
            E_chana.set("0")

    def chk_mixveg():
        if var22.get() == 1:
            mixveg_entry.configure(state=NORMAL)
            mixveg_entry.focus()
            mixveg_entry.delete('0', END)
            E_mixveg.set("")
        elif var22.get() == 0:
            mixveg_entry.configure(state=DISABLED)
            E_mixveg.set("0")

    def chk_paratha():
        if var23.get() == 1:
            paratha_entry.configure(state=NORMAL)
            paratha_entry.focus()
            paratha_entry.delete('0', END)
            E_paratha.set("")
        elif var23.get() == 0:
            paratha_entry.configure(state=DISABLED)
            E_paratha.set("0")

    def chk_laccha():
        if var24.get() == 1:
            laccha_entry.configure(state=NORMAL)
            laccha_entry.focus()
            laccha_entry.delete('0', END)
            E_laccha.set("")
        elif var24.get() == 0:
            laccha_entry.configure(state=DISABLED)
            E_laccha.set("0")

    def chk_chocolate():
        if var25.get() == 1:
            chocolate_entry.configure(state=NORMAL)
            chocolate_entry.focus()
            chocolate_entry.delete('0', END)
            E_chocolate.set("")
        elif var25.get() == 0:
            chocolate_entry.configure(state=DISABLED)
            E_chocolate.set("0")

    def chk_strawberry():
        if var26.get() == 1:
            strawberry_entry.configure(state=NORMAL)
            strawberry_entry.focus()
            strawberry_entry.delete('0', END)
            E_strawberry.set("")
        elif var26.get() == 0:
            strawberry_entry.configure(state=DISABLED)
            E_strawberry.set("0")

    def chk_pineapple():
        if var27.get() == 1:
            pineapple_entry.configure(state=NORMAL)
            pineapple_entry.focus()
            pineapple_entry.delete('0', END)
            E_pineapple.set("")
        elif var27.get() == 0:
            pineapple_entry.configure(state=DISABLED)
            E_pineapple.set("0")

    def chk_brownie():
        if var28.get() == 1:
            brownie_entry.configure(state=NORMAL)
            brownie_entry.focus()
            brownie_entry.delete('0', END)
            E_brownie.set("")
        elif var28.get() == 0:
            brownie_entry.configure(state=DISABLED)
            E_brownie.set("0")

    def chk_chocochips():
        if var29.get() == 1:
            chocochips_entry.configure(state=NORMAL)
            chocochips_entry.focus()
            chocochips_entry.delete('0', END)
            E_chocochips.set("")
        elif var29.get() == 0:
            chocochips_entry.configure(state=DISABLED)
            E_chocochips.set("0")

    def chk_vanilla():
        if var30.get() == 1:
            vanilla_entry.configure(state=NORMAL)
            vanilla_entry.focus()
            vanilla_entry.delete('0', END)
            E_vanilla.set("")
        elif var30.get() == 0:
            vanilla_entry.configure(state=DISABLED)
            E_vanilla.set("0")

    def chk_blackforest():
        if var31.get() == 1:
            blackforest_entry.configure(state=NORMAL)
            blackforest_entry.focus()
            blackforest_entry.delete('0', END)
            E_blackforest.set("")
        elif var31.get() == 0:
            blackforest_entry.configure(state=DISABLED)
            E_blackforest.set("0")

    def chk_whiteforest():
        if var32.get() == 1:
            whiteforest_entry.configure(state=NORMAL)
            whiteforest_entry.focus()
            whiteforest_entry.delete('0', END)
            E_whiteforest.set("")
        elif var32.get() == 0:
            whiteforest_entry.configure(state=DISABLED)
            E_whiteforest.set("0")

    def reset():
        SubTotal.set("")
        Paid_Tax.set("")
        Total_Cost.set("")
        Servicecharge.set("")
        Costofdrinks.set("")
        Costofstarters.set("")
        Costofmain.set("")
        Costofdessert.set("")

        E_coke.set("0")
        E_pepsi.set("0")
        E_sprite.set("0")
        E_milkshake.set("0")
        E_tea.set("0")
        E_coffee.set("0")
        E_cold_coffee.set("0")
        E_beer.set("0")

        E_manchow.set("0")
        E_tomato.set("0")
        E_manchurian.set("0")
        E_fries.set("0")
        E_noodles.set("0")
        E_paneerchilly.set("0")
        E_redpasta.set("0")
        E_whitepasta.set("0")

        E_paneer_tikka.set("0")
        E_paneer_butter.set("0")
        E_butter_roti.set("0")
        E_roti.set("0")
        E_chana.set("0")
        E_mixveg.set("0")
        E_paratha.set("0")
        E_laccha.set("0")

        E_chocolate.set("0")
        E_strawberry.set("0")
        E_pineapple.set("0")
        E_brownie.set("0")
        E_chocochips.set("0")
        E_vanilla.set("0")
        E_blackforest.set("0")
        E_whiteforest.set("0")

        var1.set(0)
        var2.set(0)
        var3.set(0)
        var4.set(0)
        var5.set(0)
        var6.set(0)
        var7.set(0)
        var8.set(0)
        var9.set(0)
        var10.set(0)
        var11.set(0)
        var12.set(0)
        var13.set(0)
        var14.set(0)
        var15.set(0)
        var16.set(0)
        var17.set(0)
        var18.set(0)
        var19.set(0)
        var20.set(0)
        var21.set(0)
        var22.set(0)
        var23.set(0)
        var24.set(0)
        var25.set(0)
        var26.set(0)
        var27.set(0)
        var28.set(0)
        var29.set(0)
        var30.set(0)
        var31.set(0)
        var32.set(0)

        coke_entry.configure(state=DISABLED)
        pepsi_entry.configure(state=DISABLED)
        sprite_entry.configure(state=DISABLED)
        milkshake_entry.configure(state=DISABLED)
        tea_entry.configure(state=DISABLED)
        coffee_entry.configure(state=DISABLED)
        cold_coffee_entry.configure(state=DISABLED)
        beer_entry.configure(state=DISABLED)

        manchow_entry.configure(state=DISABLED)
        tomato_entry.configure(state=DISABLED)
        manchurian_entry.configure(state=DISABLED)
        fries_entry.configure(state=DISABLED)
        noodles_entry.configure(state=DISABLED)
        paneerchilly_entry.configure(state=DISABLED)
        redpasta_entry.configure(state=DISABLED)
        whitepasta_entry.configure(state=DISABLED)

        paneer_tikka_entry.configure(state=DISABLED)
        paneer_butter_entry.configure(state=DISABLED)
        butter_roti_entry.configure(state=DISABLED)
        roti_entry.configure(state=DISABLED)
        chana_entry.configure(state=DISABLED)
        mixveg_entry.configure(state=DISABLED)
        paratha_entry.configure(state=DISABLED)
        laccha_entry.configure(state=DISABLED)

        chocolate_entry.configure(state=DISABLED)
        strawberry_entry.configure(state=DISABLED)
        pineapple_entry.configure(state=DISABLED)
        brownie_entry.configure(state=DISABLED)
        chocochips_entry.configure(state=DISABLED)
        vanilla_entry.configure(state=DISABLED)
        blackforest_entry.configure(state=DISABLED)
        whiteforest_entry.configure(state=DISABLED)

        txtReceipt.delete('1.0', 'end')

    def total():
        N_coke = float(E_coke.get())
        N_pepsi = float(E_pepsi.get())
        N_sprite = float(E_sprite.get())
        N_milkshake = float(E_milkshake.get())
        N_tea = float(E_tea.get())
        N_coffee = float(E_coffee.get())
        N_cold_coffee = float(E_cold_coffee.get())
        N_beer = float(E_beer.get())

        CostOfcoke = N_coke * 80
        CostOfpepsi = N_pepsi * 100
        CostOfsprite = N_sprite * 150
        CostOfmilkshake = N_milkshake * 120
        CostOftea = N_tea * 110
        CostOfcoffee = N_coffee * 90
        CostOfcold_coffee = N_cold_coffee * 130
        CostOfbeer = N_beer * 140

        costofdrinks = CostOfcoke + CostOfpepsi + CostOfsprite + CostOfmilkshake + CostOftea + CostOfcoffee + CostOfcold_coffee + CostOfbeer
        E_CostOfdrinks = "Rs. " + str('%.2f' % costofdrinks)

        N_manchow = float(E_manchow.get())
        N_tomato = float(E_tomato.get())
        N_manchurian = float(E_manchurian.get())
        N_fries = float(E_fries.get())
        N_noodles = float(E_noodles.get())
        N_paneerchilly = float(E_paneerchilly.get())
        N_redpasta = float(E_redpasta.get())
        N_whitepasta = float(E_whitepasta.get())

        CostOfmanchow = N_manchow * 200
        CostOftomato = N_tomato * 220
        CostOfmanchurian = N_manchurian * 240
        CostOffries = N_fries * 260
        CostOfnoodles = N_noodles * 300
        CostOfpaneerchilly = N_paneerchilly * 280
        CostOfredpasta = N_redpasta * 320
        CostOfwhitepasta = N_whitepasta * 500

        costofstarters = CostOfmanchow + CostOftomato + CostOfmanchurian + CostOffries + CostOfnoodles + CostOfpaneerchilly + CostOfredpasta + CostOfwhitepasta
        E_CostOfstarters = "Rs. " + str('%.2f' % costofstarters)

        N_paneer_tikka = float(E_paneer_tikka.get())
        N_paneer_butter = float(E_paneer_butter.get())
        N_butter_roti = float(E_butter_roti.get())
        N_roti = float(E_roti.get())
        N_chana = float(E_chana.get())
        N_mixveg = float(E_mixveg.get())
        N_pratha = float(E_paratha.get())
        N_laccha = float(E_laccha.get())

        CostOfpaneer_tikka = N_paneer_tikka * 250
        CostOfpaneer_butter = N_paneer_butter * 240
        CostOfbutter_roti = N_butter_roti * 220
        CostOfroti = N_roti * 200
        CostOfchana = N_chana * 160
        CostOfmixveg = N_mixveg * 180
        CostOfparatha = N_pratha * 140
        CostOflaccha = N_laccha * 120

        costofmain = CostOfpaneer_tikka + CostOfpaneer_butter + CostOfbutter_roti + CostOfroti + CostOfchana + CostOfmixveg + CostOfparatha + CostOflaccha
        E_CostOfmain = "Rs. " + str('%.2f' % costofmain)

        N_chocolate = float(E_chocolate.get())
        N_strawberry = float(E_strawberry.get())
        N_pineapple = float(E_pineapple.get())
        N_brownie = float(E_brownie.get())
        N_chocochips = float(E_chocochips.get())
        N_vanilla = float(E_vanilla.get())
        N_blackforest = float(E_blackforest.get())
        N_whiteforest = float(E_whiteforest.get())

        CostOfchocolate = N_chocolate * 80
        CostOfstrawberry = N_strawberry * 60
        CostOfpineapple = N_pineapple * 30
        CostOfbrownie = N_brownie * 30
        CostOfchocochips = N_chocochips * 80
        CostOfvanilla = N_vanilla * 70
        CostOfblackforest = N_blackforest * 70
        CostOfwhiteforest = N_whiteforest * 70

        costofdessert = CostOfchocolate + CostOfstrawberry + CostOfpineapple + CostOfbrownie + CostOfchocochips + CostOfvanilla + CostOfblackforest + CostOfwhiteforest
        E_CostOfdessert = "Rs. " + str('%.2f' % costofdessert)

        subtotal = costofdrinks + costofstarters + costofmain + costofdessert

        pay_tax = subtotal*0.2

        ser_charge = subtotal*0.1

        totalcost = ser_charge + subtotal + pay_tax

        service_charge = "Rs. " + str('%.2f' % ser_charge)
        paid_tax = "Rs. " + str('%.2f' % pay_tax)
        sub_total = "Rs. " + str('%.2f' % subtotal)
        total_cost = "Rs. " + str('%.2f' % totalcost)

        Costofdrinks.set(E_CostOfdrinks)
        Costofstarters.set(E_CostOfstarters)
        Costofmain.set(E_CostOfmain)
        Costofdessert.set(E_CostOfdessert)
        SubTotal.set(sub_total)
        Paid_Tax.set(paid_tax)
        Total_Cost.set(total_cost)
        Servicecharge.set(service_charge)

        x = random.randint(100, 10000)
        billnumber = 'BILL' + str(x)
        date_bill = time.strftime('%d/%m/%y')
        txtReceipt.insert(END, '******************************************************************************************\n')
        txtReceipt.insert(END, "Hotel Bliss Fort \n")
        txtReceipt.insert(END, "Hotel E-mail ID: hotelblissfort@gmail.com \n")
        txtReceipt.insert(END, "Hotel Contact Number 1: +91 XXX-XXX-XXXX \n")
        txtReceipt.insert(END, "Hotel Contact Number 2: +91 000-000-0000 \n")
        txtReceipt.insert(END, '******************************************************************************************\n')
        txtReceipt.insert(END, 'Receipt Ref:\t\t' + billnumber + '\t\t' + date_bill + '\n')
        txtReceipt.insert(END, '******************************************************************************************\n')
        txtReceipt.insert(END, '{0:<45}{1:<15}{2}\n'.format('Items', 'Quantity', 'Amount'))
        txtReceipt.insert(END, '******************************************************************************************\n')
        if E_coke.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Coke', str(E_coke.get()), str(CostOfcoke)))
        if E_pepsi.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Pepsi', str(E_pepsi.get()), str(CostOfpepsi)))
        if E_sprite.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Sprite', str(E_sprite.get()), str(CostOfsprite)))
        if E_milkshake.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Milkshake', str(E_milkshake.get()), str(CostOfmilkshake)))
        if E_tea.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Tea', str(E_tea.get()), str(CostOftea)))
        if E_coffee.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Coffee', str(E_coffee.get()), str(CostOfcoffee)))
        if E_cold_coffee.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Cold Coffee', str(E_cold_coffee.get()), str(CostOfcold_coffee)))
        if E_beer.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Beer', str(E_beer.get()), str(CostOfbeer)))
        if E_manchow.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Manchow Soup', str(E_manchow.get()), str(CostOfmanchow)))
        if E_tomato.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Tomato Soup', str(E_tomato.get()), str(CostOftomato)))
        if E_manchurian.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Manchurian', str(E_manchurian.get()), str(CostOfmanchurian)))
        if E_fries.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('French Fries', str(E_fries.get()), str(CostOffries)))
        if E_noodles.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Noodles', str(E_noodles.get()), str(CostOfnoodles)))
        if E_paneerchilly.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Paneer Chilly', str(E_paneerchilly.get()), str(CostOfpaneerchilly)))
        if E_redpasta.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Red Sauce Pasta', str(E_redpasta.get()), str(CostOfredpasta)))
        if E_whitepasta.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('White Sauce Pasta', str(E_whitepasta.get()), str(CostOfwhitepasta)))
        if E_paneer_tikka.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Paneer Tikka Masala', str(E_paneer_tikka.get()), str(CostOfpaneer_tikka)))
        if E_paneer_butter.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Paneer Butter Masala', str(E_paneer_butter.get()), str(CostOfpaneer_butter)))
        if E_butter_roti.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Butter Roti', str(E_butter_roti.get()), str(CostOfbutter_roti)))
        if E_roti.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Plain Roti', str(E_roti.get()), str(CostOfroti)))
        if E_chana.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Chana Masala', str(E_chana.get()), str(CostOfchana)))
        if E_mixveg.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Mixed Veg', str(E_mixveg.get()), str(CostOfmixveg)))
        if E_paratha.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Plain Paratha', str(E_paratha.get()), str(CostOfparatha)))
        if E_laccha.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Laccha Paratha', str(E_laccha.get()), str(CostOflaccha)))
        if E_chocolate.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Chocolate Cake', str(E_chocolate.get()), str(CostOfchocolate)))
        if E_strawberry.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Strawberry Cake', str(E_strawberry.get()), str(CostOfstrawberry)))
        if E_pineapple.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Pineapple Cake', str(E_pineapple.get()), str(CostOfpineapple)))
        if E_brownie.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Choco Brownie', str(E_brownie.get()), str(CostOfbrownie)))
        if E_chocochips.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Choco Chips Ice-Cream', str(E_chocochips.get()), str(CostOfchocochips)))
        if E_vanilla.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Vanilla Ice-Cream', str(E_vanilla.get()), str(CostOfvanilla)))
        if E_blackforest.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('Black Forest Cake', str(E_blackforest.get()), str(CostOfblackforest)))
        if E_whiteforest.get() != '0':
            txtReceipt.insert(END, '{0:<50}{1:<20}{2}\n'.format('White Forest Cake', str(E_whiteforest.get()), str(CostOfwhiteforest)))
        txtReceipt.insert(END, '******************************************************************************************\n')
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Cost Of Drinks:", Costofdrinks.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Cost Of Starters:", Costofstarters.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Cost Of Main Course:", Costofmain.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Cost Of Dessert:", Costofdessert.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Tax Paid:", Paid_Tax.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Sub Total:", SubTotal.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Service Tax:", Servicecharge.get()))
        txtReceipt.insert(END, '{0:<50}{1}\n'.format("Total Amount:", Total_Cost.get()))

        try:
            fopen = open("Bill.txt", 'w')
        except FileNotFoundError:
            print("Error")
        else:
            fopen.write('******************************************************************************************\n')
            fopen.write("Hotel Bliss Fort \n")
            fopen.write("Hotel E-mail ID: hotelblissfort@gmail.com \n")
            fopen.write("Hotel Contact Number 1: +91 XXX-XXX-XXXX \n")
            fopen.write("Hotel Contact Number 2: +91 000-000-0000 \n")
            fopen.write('******************************************************************************************\n')
            fopen.write('Receipt Ref:\t\t' + billnumber + '\t\t' + date_bill + '\n')
            fopen.write('******************************************************************************************\n')
            fopen.write('{0:<45}{1:<15}{2}\n'.format('Items', 'Quantity', 'Amount'))
            fopen.write('******************************************************************************************\n')
            if E_coke.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Coke', str(E_coke.get()), str(CostOfcoke)))
            if E_pepsi.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Pepsi', str(E_pepsi.get()), str(CostOfpepsi)))
            if E_sprite.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Sprite', str(E_sprite.get()), str(CostOfsprite)))
            if E_milkshake.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Milkshake', str(E_milkshake.get()), str(CostOfmilkshake)))
            if E_tea.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Tea', str(E_tea.get()), str(CostOftea)))
            if E_coffee.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Coffee', str(E_coffee.get()), str(CostOfcoffee)))
            if E_cold_coffee.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Cold Coffee', str(E_cold_coffee.get()), str(CostOfcold_coffee)))
            if E_beer.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Beer', str(E_beer.get()), str(CostOfbeer)))
            if E_manchow.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Manchow Soup', str(E_manchow.get()), str(CostOfmanchow)))
            if E_tomato.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Tomato Soup', str(E_tomato.get()), str(CostOftomato)))
            if E_manchurian.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Manchurian', str(E_manchurian.get()), str(CostOfmanchurian)))
            if E_fries.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('French Fries', str(E_fries.get()), str(CostOffries)))
            if E_noodles.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Noodles', str(E_noodles.get()), str(CostOfnoodles)))
            if E_paneerchilly.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Paneer Chilly', str(E_paneerchilly.get()), str(CostOfpaneerchilly)))
            if E_redpasta.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Red Sauce Pasta', str(E_redpasta.get()), str(CostOfredpasta)))
            if E_whitepasta.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('White Sauce Pasta', str(E_whitepasta.get()), str(CostOfwhitepasta)))
            if E_paneer_tikka.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Paneer Tikka Masala', str(E_paneer_tikka.get()), str(CostOfpaneer_tikka)))
            if E_paneer_butter.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Paneer Butter Masala', str(E_paneer_butter.get()), str(CostOfpaneer_butter)))
            if E_butter_roti.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Butter Roti', str(E_butter_roti.get()), str(CostOfbutter_roti)))
            if E_roti.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Plain Roti', str(E_roti.get()), str(CostOfroti)))
            if E_chana.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Chana Masala', str(E_chana.get()), str(CostOfchana)))
            if E_mixveg.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Mixed Veg', str(E_mixveg.get()), str(CostOfmixveg)))
            if E_paratha.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Plain Paratha', str(E_paratha.get()), str(CostOfparatha)))
            if E_laccha.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Laccha Paratha', str(E_laccha.get()), str(CostOflaccha)))
            if E_chocolate.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Chocolate Cake', str(E_chocolate.get()), str(CostOfchocolate)))
            if E_strawberry.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Strawberry Cake', str(E_strawberry.get()), str(CostOfstrawberry)))
            if E_pineapple.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Pineapple Cake', str(E_pineapple.get()), str(CostOfpineapple)))
            if E_brownie.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Choco Brownie', str(E_brownie.get()), str(CostOfbrownie)))
            if E_chocochips.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Choco Chips Ice-Cream', str(E_chocochips.get()), str(CostOfchocochips)))
            if E_vanilla.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Vanilla Ice-Cream', str(E_vanilla.get()), str(CostOfvanilla)))
            if E_blackforest.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('Black Forest Cake', str(E_blackforest.get()), str(CostOfblackforest)))
            if E_whiteforest.get() != '0':
                fopen.write('{0:<50}{1:<20}{2}\n'.format('White Forest Cake', str(E_whiteforest.get()), str(CostOfwhiteforest)))
            fopen.write('******************************************************************************************\n')
            fopen.write('{0:<50}{1}\n'.format("Cost Of Drinks:", Costofdrinks.get()))
            fopen.write('{0:<50}{1}\n'.format("Cost Of Starters:", Costofstarters.get()))
            fopen.write('{0:<50}{1}\n'.format("Cost Of Main Course:", Costofmain.get()))
            fopen.write('{0:<50}{1}\n'.format("Cost Of Dessert:", Costofdessert.get()))
            fopen.write('{0:<50}{1}\n'.format("Tax Paid:", Paid_Tax.get()))
            fopen.write('{0:<50}{1}\n'.format("Sub Total:", SubTotal.get()))
            fopen.write('{0:<50}{1}\n'.format("Service Tax:", Servicecharge.get()))
            fopen.write('{0:<50}{1}\n'.format("Total Amount:", Total_Cost.get()))

            fopen.close()

    drink_frame = LabelFrame(menu_frame, text='Drinks', bd=5, relief=SUNKEN, font=('Helvatica Bold', 11), bg='#d2e3f2')
    drink_frame.grid(row=0, column=0)
    starter_frame = LabelFrame(menu_frame, text='Starter', bd=5, relief=SUNKEN, font=('Helvatica Bold', 11), bg='#d2e3f2')
    starter_frame.grid(row=0, column=1)
    maincourse_frame = LabelFrame(menu_frame, text='Main Course', bd=5, relief=SUNKEN, font=('Helvatica Bold', 11), bg='#d2e3f2')
    maincourse_frame.grid(row=0, column=2)
    dessert_frame = LabelFrame(menu_frame, text='Dessert', bd=5, relief=SUNKEN, font=('Helvatica Bold', 11), bg='#d2e3f2')
    dessert_frame.grid(row=0, column=3)

    #Drink Frame Check Buttons
    coke_check = Checkbutton(drink_frame, text='Coke', onvalue=1, offvalue=0, variable=var1, command=chk_coke, font=('Helvatica Bold', 10), bg='#d2e3f2')
    coke_check.grid(row=0, column=0, sticky=W, padx=5)
    pepsi_check = Checkbutton(drink_frame, text='Pepsi', onvalue=1, offvalue=0, variable=var2, command=chk_pepsi, font=('Helvatica Bold', 10), bg='#d2e3f2')
    pepsi_check.grid(row=1, column=0, sticky=W, padx=5)
    sprite_check = Checkbutton(drink_frame, text='Sprite', onvalue=1, offvalue=0, variable=var3, command=chk_sprite, font=('Helvatica Bold', 10), bg='#d2e3f2')
    sprite_check.grid(row=2, column=0, sticky=W, padx=5)
    milkshake_check = Checkbutton(drink_frame, text='Milkshake', onvalue=1, offvalue=0, variable=var4, command=chk_milkshake, font=('Helvatica Bold', 10), bg='#d2e3f2')
    milkshake_check.grid(row=3, column=0, sticky=W, padx=5)
    tea_check = Checkbutton(drink_frame, text='Tea', onvalue=1, offvalue=0, variable=var5, command=chk_tea, font=('Helvatica Bold', 10), bg='#d2e3f2')
    tea_check.grid(row=4, column=0, sticky=W, padx=5)
    coffee_check = Checkbutton(drink_frame, text='Coffee', onvalue=1, offvalue=0, variable=var6, command=chk_coffee, font=('Helvatica Bold', 10), bg='#d2e3f2')
    coffee_check.grid(row=5, column=0, sticky=W, padx=5)
    cold_coffee_check = Checkbutton(drink_frame, text='Cold Coffee', onvalue=1, offvalue=0, variable=var7, command=chk_cold_coffee, font=('Helvatica Bold', 10), bg='#d2e3f2')
    cold_coffee_check.grid(row=6, column=0, sticky=W, padx=5)
    beer_check = Checkbutton(drink_frame, text='Beer', onvalue=1, offvalue=0, variable=var8, command=chk_beer, font=('Helvatica Bold', 10), bg='#d2e3f2')
    beer_check.grid(row=7, column=0, sticky=W, padx=5)

    #Drink Frame Entry
    coke_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_coke, font=('Helvatica Bold', 10))
    coke_entry.grid(row=0, column=1, sticky=E, padx=5)
    pepsi_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_pepsi, font=('Helvatica Bold', 10))
    pepsi_entry.grid(row=1, column=1, sticky=E, padx=5)
    sprite_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_sprite, font=('Helvatica Bold', 10))
    sprite_entry.grid(row=2, column=1, sticky=E, padx=5)
    milkshake_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_milkshake, font=('Helvatica Bold', 10))
    milkshake_entry.grid(row=3, column=1, sticky=E, padx=5)
    tea_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_tea, font=('Helvatica Bold', 10))
    tea_entry.grid(row=4, column=1, sticky=E, padx=5)
    coffee_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_coffee, font=('Helvatica Bold', 10))
    coffee_entry.grid(row=5, column=1, sticky=E, padx=5)
    cold_coffee_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_cold_coffee, font=('Helvatica Bold', 10))
    cold_coffee_entry.grid(row=6, column=1, sticky=E, padx=5)
    beer_entry = Entry(drink_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_beer, font=('Helvatica Bold', 10))
    beer_entry.grid(row=7, column=1, sticky=E, padx=5)

    # Starters Frame Check Buttons
    manchow_check = Checkbutton(starter_frame, text='Manchow Soup', onvalue=1, offvalue=0, variable=var9, command=chk_manchow, font=('Helvatica Bold', 10), bg='#d2e3f2')
    manchow_check.grid(row=0, column=0, sticky=W, padx=5)
    tomato_check = Checkbutton(starter_frame, text='Tomato Soup', onvalue=1, offvalue=0, variable=var10, command=chk_tomato, font=('Helvatica Bold', 10), bg='#d2e3f2')
    tomato_check.grid(row=1, column=0, sticky=W, padx=5)
    manchurian_check = Checkbutton(starter_frame, text='Manchurian', onvalue=1, offvalue=0, variable=var11, command=chk_manchurian, font=('Helvatica Bold', 10), bg='#d2e3f2')
    manchurian_check.grid(row=2, column=0, sticky=W, padx=5)
    fries_check = Checkbutton(starter_frame, text='French Fries', onvalue=1, offvalue=0, variable=var12, command=chk_fries, font=('Helvatica Bold', 10), bg='#d2e3f2')
    fries_check.grid(row=3, column=0, sticky=W, padx=5)
    noodles_check = Checkbutton(starter_frame, text='Noodles', onvalue=1, offvalue=0, variable=var13, command=chk_noodles, font=('Helvatica Bold', 10), bg='#d2e3f2')
    noodles_check.grid(row=4, column=0, sticky=W, padx=5)
    paneerchilly_check = Checkbutton(starter_frame, text='Paneer Chilly', onvalue=1, offvalue=0, variable=var14, command=chk_paneerchilly, font=('Helvatica Bold', 10), bg='#d2e3f2')
    paneerchilly_check.grid(row=5, column=0, sticky=W, padx=5)
    redpasta_check = Checkbutton(starter_frame, text='Red Sauce Pasta', onvalue=1, offvalue=0, variable=var15, command=chk_redpasta, font=('Helvatica Bold', 10), bg='#d2e3f2')
    redpasta_check.grid(row=6, column=0, sticky=W, padx=5)
    whitepaste_check = Checkbutton(starter_frame, text='White Sauce Pasta', onvalue=1, offvalue=0, variable=var16, command=chk_whitepasta, font=('Helvatica Bold', 10), bg='#d2e3f2')
    whitepaste_check.grid(row=7, column=0, sticky=W, padx=5)

    # Starters Frame Entry
    manchow_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_manchow, font=('Helvatica Bold', 10))
    manchow_entry.grid(row=0, column=1, sticky=E, padx=5)
    tomato_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_tomato, font=('Helvatica Bold', 10))
    tomato_entry.grid(row=1, column=1, sticky=E, padx=5)
    manchurian_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_manchurian, font=('Helvatica Bold', 10))
    manchurian_entry.grid(row=2, column=1, sticky=E, padx=5)
    fries_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_fries, font=('Helvatica Bold', 10))
    fries_entry.grid(row=3, column=1, sticky=E, padx=5)
    noodles_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_noodles, font=('Helvatica Bold', 10))
    noodles_entry.grid(row=4, column=1, sticky=E, padx=5)
    paneerchilly_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_paneerchilly, font=('Helvatica Bold', 10))
    paneerchilly_entry.grid(row=5, column=1, sticky=E, padx=5)
    redpasta_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_redpasta, font=('Helvatica Bold', 10))
    redpasta_entry.grid(row=6, column=1, sticky=E, padx=5)
    whitepasta_entry = Entry(starter_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_whitepasta, font=('Helvatica Bold', 10))
    whitepasta_entry.grid(row=7, column=1, sticky=E, padx=5)

    # Main Course Frame Check Buttons
    paneer_tikka_check = Checkbutton(maincourse_frame, text='Paneer Tikka Masala', onvalue=1, offvalue=0, variable=var17, command=chk_paneer_tikka, font=('Helvatica Bold', 10), bg='#d2e3f2')
    paneer_tikka_check.grid(row=0, column=0, sticky=W, padx=5)
    paneer_butter_check = Checkbutton(maincourse_frame, text='Paneer Butter Msala', onvalue=1, offvalue=0, variable=var18, command=chk_paneer_butter, font=('Helvatica Bold', 10), bg='#d2e3f2')
    paneer_butter_check.grid(row=1, column=0, sticky=W, padx=5)
    butter_roti_check = Checkbutton(maincourse_frame, text='Butter Roti', onvalue=1, offvalue=0, variable=var19, command=chk_butter_roti, font=('Helvatica Bold', 10), bg='#d2e3f2')
    butter_roti_check.grid(row=2, column=0, sticky=W, padx=5)
    roti_check = Checkbutton(maincourse_frame, text='Plain Roti', onvalue=1, offvalue=0, variable=var20, command=chk_roti, font=('Helvatica Bold', 10), bg='#d2e3f2')
    roti_check.grid(row=3, column=0, sticky=W, padx=5)
    chana_check = Checkbutton(maincourse_frame, text='Chana Masala', onvalue=1, offvalue=0, variable=var21, command=chk_chana, font=('Helvatica Bold', 10), bg='#d2e3f2')
    chana_check.grid(row=4, column=0, sticky=W, padx=5)
    mixveg_check = Checkbutton(maincourse_frame, text='Mixed Veg', onvalue=1, offvalue=0, variable=var22, command=chk_mixveg, font=('Helvatica Bold', 10), bg='#d2e3f2')
    mixveg_check.grid(row=5, column=0, sticky=W, padx=5)
    paratha_check = Checkbutton(maincourse_frame, text='Plain Paratha', onvalue=1, offvalue=0, variable=var23, command=chk_paratha, font=('Helvatica Bold', 10), bg='#d2e3f2')
    paratha_check.grid(row=6, column=0, sticky=W, padx=5)
    laccha_check = Checkbutton(maincourse_frame, text='Laccha Paratha', onvalue=1, offvalue=0, variable=var24, command=chk_laccha, font=('Helvatica Bold', 10), bg='#d2e3f2')
    laccha_check.grid(row=7, column=0, sticky=W, padx=5)

    # Main Course Frame Entry
    paneer_tikka_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_paneer_tikka, font=('Helvatica Bold', 10))
    paneer_tikka_entry.grid(row=0, column=1, sticky=E, padx=5)
    paneer_butter_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_paneer_butter, font=('Helvatica Bold', 10))
    paneer_butter_entry.grid(row=1, column=1, sticky=E, padx=5)
    butter_roti_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_butter_roti, font=('Helvatica Bold', 10))
    butter_roti_entry.grid(row=2, column=1, sticky=E, padx=5)
    roti_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_roti, font=('Helvatica Bold', 10))
    roti_entry.grid(row=3, column=1, sticky=E, padx=5)
    chana_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_chana, font=('Helvatica Bold', 10))
    chana_entry.grid(row=4, column=1, sticky=E, padx=5)
    mixveg_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_mixveg, font=('Helvatica Bold', 10))
    mixveg_entry.grid(row=5, column=1, sticky=E, padx=5)
    paratha_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_paratha, font=('Helvatica Bold', 10))
    paratha_entry.grid(row=6, column=1, sticky=E, padx=5)
    laccha_entry = Entry(maincourse_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_laccha, font=('Helvatica Bold', 10))
    laccha_entry.grid(row=7, column=1, sticky=E, padx=5)

    # Dessert Frame Check Buttons
    chocolate_check = Checkbutton(dessert_frame, text='Chocolate Cake', onvalue=1, offvalue=0, variable=var25, command=chk_chocolate, font=('Helvatica Bold', 10), bg='#d2e3f2')
    chocolate_check.grid(row=0, column=0, sticky=W, padx=5)
    strawberry_check = Checkbutton(dessert_frame, text='Strawberry Cake', onvalue=1, offvalue=0, variable=var26, command=chk_strawberry, font=('Helvatica Bold', 10), bg='#d2e3f2')
    strawberry_check.grid(row=1, column=0, sticky=W, padx=5)
    pineapple_check = Checkbutton(dessert_frame, text='Pineapple Cake', onvalue=1, offvalue=0, variable=var27, command=chk_pineapple, font=('Helvatica Bold', 10), bg='#d2e3f2')
    pineapple_check.grid(row=2, column=0, sticky=W, padx=5)
    brownie_check = Checkbutton(dessert_frame, text='Choco Brownie', onvalue=1, offvalue=0, variable=var28, command=chk_brownie, font=('Helvatica Bold', 10), bg='#d2e3f2')
    brownie_check.grid(row=3, column=0, sticky=W, padx=5)
    chocochips_check = Checkbutton(dessert_frame, text='Choco Chips Ice-Cream', onvalue=1, offvalue=0, variable=var29, command=chk_chocochips, font=('Helvatica Bold', 10), bg='#d2e3f2')
    chocochips_check.grid(row=4, column=0, sticky=W, padx=5)
    vanilla_check = Checkbutton(dessert_frame, text='Vanilla Ice-Cream', onvalue=1, offvalue=0, variable=var30, command=chk_vanilla, font=('Helvatica Bold', 10), bg='#d2e3f2')
    vanilla_check.grid(row=5, column=0, sticky=W, padx=5)
    blackforest_check = Checkbutton(dessert_frame, text='Black Forest Cake', onvalue=1, offvalue=0, variable=var31, command=chk_blackforest, font=('Helvatica Bold', 10), bg='#d2e3f2')
    blackforest_check.grid(row=6, column=0, sticky=W, padx=5)
    whiteforest_check = Checkbutton(dessert_frame, text='White Forest Cake', onvalue=1, offvalue=0, variable=var32, command=chk_whiteforest, font=('Helvatica Bold', 10), bg='#d2e3f2')
    whiteforest_check.grid(row=7, column=0, sticky=W, padx=5)

    # Dessert Frame Entry
    chocolate_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_chocolate, font=('Helvatica Bold', 10))
    chocolate_entry.grid(row=0, column=1, sticky=E, padx=5)
    strawberry_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_strawberry, font=('Helvatica Bold', 10))
    strawberry_entry.grid(row=1, column=1, sticky=E, padx=5)
    pineapple_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_pineapple, font=('Helvatica Bold', 10))
    pineapple_entry.grid(row=2, column=1, sticky=E, padx=5)
    brownie_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_brownie, font=('Helvatica Bold', 10))
    brownie_entry.grid(row=3, column=1, sticky=E, padx=5)
    chocochips_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_chocochips, font=('Helvatica Bold', 10))
    chocochips_entry.grid(row=4, column=1, sticky=E, padx=5)
    vanilla_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_vanilla, font=('Helvatica Bold', 10))
    vanilla_entry.grid(row=5, column=1, sticky=E, padx=5)
    blackforest_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_blackforest, font=('Helvatica Bold', 10))
    blackforest_entry.grid(row=6, column=1, sticky=E, padx=5)
    whiteforest_entry = Entry(dessert_frame, width=5, state=DISABLED, relief=SUNKEN, textvariable=E_whiteforest, font=('Helvatica Bold', 10))
    whiteforest_entry.grid(row=7, column=1, sticky=E, padx=5)

    #Payment Info Frame Content
    lblCostOfDrinks = Label(cost_frame, text='Cost Of Drinks', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblCostOfDrinks.grid(row=0, column=0, padx=5)
    txtCostOfDrinks = Entry(cost_frame, textvariable=Costofdrinks, font=('Helvatica Bold', 10))
    txtCostOfDrinks.grid(row=0, column=1, padx=5)

    lblCostOfStarters = Label(cost_frame, text='Cost Of Starters', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblCostOfStarters.grid(row=1, column=0, padx=5)
    txtCostOfStarters = Entry(cost_frame, textvariable=Costofstarters, font=('Helvatica Bold', 10))
    txtCostOfStarters.grid(row=1, column=1, padx=5)

    lblCostOfMain = Label(cost_frame, text='Cost Of Main Course', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblCostOfMain.grid(row=2, column=0, padx=5)
    txtCostOfMain = Entry(cost_frame, textvariable=Costofmain, font=('Helvatica Bold', 10))
    txtCostOfMain.grid(row=2, column=1, padx=5)

    lblCostOfDessert = Label(cost_frame, text='Cost Of Dessert', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblCostOfDessert.grid(row=3, column=0, padx=5)
    txtCostOfDessert = Entry(cost_frame, textvariable=Costofdessert, font=('Helvatica Bold', 10))
    txtCostOfDessert.grid(row=3, column=1, padx=5)

    lblPaidTax = Label(cost_frame, text='Paid Tax', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblPaidTax.grid(row=0, column=2, padx=5)
    txtPaidTax = Entry(cost_frame, insertwidth=2, textvariable=Paid_Tax, font=('Helvatica Bold', 10))
    txtPaidTax.grid(row=0, column=3, padx=5)

    lblSubTotal = Label(cost_frame, text='Sub Total', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblSubTotal.grid(row=1, column=2, padx=5)
    txtSubTotal = Entry(cost_frame, textvariable=SubTotal, font=('Helvatica Bold', 10))
    txtSubTotal.grid(row=1, column=3, padx=5)

    lblServiceCharge = Label(cost_frame, text='Service Charge', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblServiceCharge.grid(row=2, column=2, padx=5)
    txtServiceCharge = Entry(cost_frame, textvariable=Servicecharge, font=('Helvatica Bold', 10))
    txtServiceCharge.grid(row=2, column=3, padx=5)

    lblTotalCost = Label(cost_frame, text='Total Cost', font=('Helvatica Bold', 10), bg='#d2e3f2')
    lblTotalCost.grid(row=3, column=2, padx=5)
    txtTotalCost = Entry(cost_frame, textvariable=Total_Cost, font=('Helvatica Bold', 10))
    txtTotalCost.grid(row=3, column=3, padx=5)

    btnTotal = Button(button_frame, text="Total", bd=5, relief=RIDGE, command=total, font=('Helvatica Bold', 10))
    btnTotal.grid(row=0, column=0, padx=5, pady=5)
    btnreset = Button(button_frame, text="Reset", bd=5, relief=RIDGE, command=reset, font=('Helvatica Bold', 10))
    btnreset.grid(row=0, column=2, padx=5, pady=5)

    #Bill
    txtReceipt = Text(bill_frame, width=65, height=20, bg='white', bd=5, font=('arial', 10, 'bold'))
    txtReceipt.grid(row=0, column=0)


def def_records():

    def filter():
        arr = [0, 0, 0, 0]

        if floor_num.get() != 'None':
            arr[0] = int(floor_num.get())

        if bed_num.get() != 'None':
            arr[1] = int(bed_num.get())

        if entry_date_value.get():
            arr[2] = datetime.datetime.strptime(str(entry_date_value.get()), "%m/%d/%y")
            arr[2] = arr[2].strftime("%d-%b-%y")
            print("arr2", arr[2])

        if exit_date_value.get():
            arr[3] = datetime.datetime.strptime(str(exit_date_value.get()), "%m/%d/%y")
            arr[3] = arr[3].strftime("%d-%b-%y")
            print("arr3", arr[3])

        sql = "SELECT * FROM customer"
        flag = 0

        if arr[0] != 0:
            sql += " WHERE "
            flag = 1
            if arr[0] == 1:
                sql += "Room_num in (101, 102, 103, 104)"
            elif arr[0] == 2:
                sql += "Room_num in (201, 202, 203, 204)"
            elif arr[0] == 3:
                sql += "Room_num in (301, 302, 303, 304)"
            elif arr[0] == 4:
                sql += "Room_num in (401, 402, 403, 404)"
            elif arr[0] == 5:
                sql += "Room_num in (501, 502, 503, 504)"
            elif arr[0] == 6:
                sql += "Room_num in (601, 602, 603, 604)"
            elif arr[0] == 7:
                sql += "Room_num in (701, 702, 703, 704)"
            elif arr[0] == 8:
                sql += "Room_num in (801, 802, 803, 804)"
            elif arr[0] == 9:
                sql += "Room_num in (901, 902, 903, 904)"
            else:
                sql += "Room_num in (1001, 1002, 1003, 1004)"

        if arr[1] != 0:
            if flag == 0:
                sql += " WHERE "
                flag = 1
            else:
                sql += " AND "

            sql += f"Beds={arr[1]}"

        if arr[2] != 0:
            if flag == 0:
                sql += " WHERE "
                flag = 1
            else:
                sql += " AND "

            sql += f"Check_in >= '{arr[2]}'"

        if arr[3] != 0:
            if flag == 0:
                sql += " WHERE "
                flag = 1
            else:
                sql += " AND "

            sql += f"Check_in <= '{arr[3]}'"

        try:
            with cx_Oracle.connect(user="demopython",
                                   password="himanshu",
                                   dsn="localhost/xepdb1") as connection:
                with connection.cursor() as cursor:
                    x = cursor.execute(sql)

                    data = x.fetchall()
                    record_frame.delete(1.0, END)

                    if len(data) != 0:

                        for i in data:
                            record_frame.insert(END, "{0:15}{1:15}{2:15}{3:15}{4:15}\n\n".format(i[0], i[1], i[2], i[3], i[4]))
                            record_frame.insert(END, ("*"*80)+"\n")

        except cx_Oracle.Error as error:
            print('Error Occured:')
            print(error)

    def reset():
        floor_num.set('None')
        bed_num.set('None')
        record_frame.delete('1.0', 'end')
        entry_date_value.delete(0, 'end')
        exit_date_value.delete(0, 'end')

    floor_num = StringVar()
    floor_num.set('None')
    floors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    bed_num = StringVar()
    bed_num.set('None')
    beds = ['1', '2', '3']

    today_date = date.today()

    #overall_rating = StringVar()
    #overall_rating.set('0')

    dropdown_frame = Frame(main_frame, bd=5, width=1200, height=50, relief=RIDGE, bg='#f2f3d2')
    dropdown_frame.grid(row=0, column=0)

    filter_floor = Label(dropdown_frame, text="Floor No.:", bg='#f2f3d2')
    filter_floor.grid(row=0, column=0)
    floor_filter_value = OptionMenu(dropdown_frame, floor_num, *floors)
    floor_filter_value.grid(row=0, column=1, padx=2, pady=2)

    filter_beds = Label(dropdown_frame, text="No. of Beds:", bg='#f2f3d2')
    filter_beds.grid(row=0, column=2)
    bed_filter_value = OptionMenu(dropdown_frame, bed_num, *beds)
    bed_filter_value.grid(row=0, column=3, padx=2, pady=2)

    filter_entry_date = Label(dropdown_frame, text="Check-In Date:", bg='#f2f3d2')
    filter_entry_date.grid(row=0, column=4)
    entry_date_value = DateEntry(dropdown_frame, selectmode='day', year=today_date.year, month=today_date.month, day=today_date.day)
    entry_date_value.grid(row=0, column=5, padx=2, pady=2)
    entry_date_value.delete(0, 'end')

    filter_exit_date = Label(dropdown_frame, text="To", bg='#f2f3d2')
    filter_exit_date.grid(row=0, column=6)
    exit_date_value = DateEntry(dropdown_frame, selectmode='day', year=today_date.year, month=today_date.month, day=today_date.day)
    exit_date_value.grid(row=0, column=7, padx=2, pady=2)
    exit_date_value.delete(0, 'end')

    filter_button = Button(dropdown_frame, text="Filter", bd=4, command=filter)
    filter_button.grid(row=0, column=8)

    reset_button = Button(dropdown_frame, text="Reset", bd=4, command=reset)
    reset_button.grid(row=0, column=9)

    record_frame = Text(main_frame, bd=5, width=150, height=30, border=4, relief=SUNKEN, font=('Helvatica Bold', 11))
    record_frame.grid(row=1, column=0, padx=2, pady=2)


def def_final_bill():

    def CheckOut():
        # UPDATE DATABASE AND SET CHECKOUT DATE TO CURRENT DATE AND PRINT THE BILL ON SCREEN AS WELL AS IN A TXT FILE
        selected_name = name.get()
        print(selected_name)
        index = 0
        for identity in range(len(data)):
            if data[identity][0] == selected_name:
                index = identity

        selected_number = int(data[index][1])
        current_room = int(data[index][3])

        check_out = date.today()
        print(check_out)
        check_out = datetime.datetime.strptime(str(check_out), "%Y-%m-%d")
        check_out = check_out.strftime("%d-%b-%y")
        print(check_out)

        update_op(selected_name, selected_number, check_out)

        query = f"SELECT sysdate-Check_in FROM customer WHERE name = '{selected_name}'"

        try:
            with cx_Oracle.connect(user="demopython",
                                   password="himanshu",
                                   dsn="localhost/xepdb1") as connection:
                with connection.cursor() as cursor:
                    x = cursor.execute(query)
                    x = x.fetchall()

                    print("Blah")
                    days = math.ceil(x[0][0])
                    print(math.ceil(x[0][0]))

        except cx_Oracle.Error as error:
            print('Error Occured:')
            print(error)

        if current_room in single_bed_occupied:
            single_bed_available_rooms.append(single_bed_occupied.pop(single_bed_occupied.index(current_room)))
        elif current_room in double_bed_occupied:
            double_bed_available_rooms.append(double_bed_occupied.pop(double_bed_occupied.index(current_room)))
        elif current_room in triple_bed_occupied:
            triple_bed_available_rooms.append(triple_bed_occupied.pop(triple_bed_occupied.index(current_room)))

        if int(data[index][2]) == 1:
            price = 800
        elif int(data[index][2]) == 2:
            price = 1500
        else:
            price = 2000

        bill_text = """Name:{}\nPhone Number:{}\nRoom Number:{}\nNumber Of Beds:{}\n""".format(selected_name, selected_number, data[index][3], data[index][2])
        final_bill_text.insert(END, ("*" * 50) + "\n")
        final_bill_text.insert(END, "Hotel Bliss Fort \n")
        final_bill_text.insert(END, "Hotel E-mail ID: hotelblissfort@gmail.com \n")
        final_bill_text.insert(END, "Hotel Contact Number 1: +91 XXX-XXX-XXXX \n")
        final_bill_text.insert(END, "Hotel Contact Number 2: +91 000-000-0000 \n")
        final_bill_text.insert(END, ("*"*50)+"\n")
        final_bill_text.insert(END, bill_text+"\n")
        final_bill_text.insert(END, ("*"*50) + "\n")
        final_bill_text.insert(END, str(price*days) + "\n")
        final_bill_text.insert(END, ("*"*50) + "\n")

        fopen = open('final_bill.txt', 'w')
        fopen.write(("*" * 50) + "\n")
        fopen.write("Hotel Bliss Fort \n")
        fopen.write("Hotel E-mail ID: hotelblissfort@gmail.com \n")
        fopen.write("Hotel Contact Number 1: +91 XXX-XXX-XXXX \n")
        fopen.write("Hotel Contact Number 2: +91 000-000-0000 \n")
        fopen.write(("*" * 50) + "\n")
        fopen.write(bill_text + "\n")
        fopen.write(("*" * 50) + "\n")
        fopen.write(str(price*days) + "\n")
        fopen.write(("*" * 50) + "\n")
        fopen.close()

    def extraction():
        extract_name = name.get()

        for j in data:
            if j[0] == extract_name:
                Label(details_frame, text="Name:{}".format(j[0]), bg='#f2f3d2').grid(row=1, column=0, columnspan=2)
                Label(details_frame, text="Phone Number:{}".format(j[1]), bg='#f2f3d2').grid(row=2, column=0, columnspan=2)
                Label(details_frame, text="Room Number:{}".format(j[3]), bg='#f2f3d2').grid(row=3, column=0, columnspan=2)
                break

    # EXTRACT THE DATA FROM DATABASE AND DISPLAY NAMES OF ONLY THOSE PRESENTLY CHECKED-IN IN THE HOTEL IN A DROPDOWN BOX
    data = select_op()

    name = StringVar()
    name.set('Select')

    names = []

    for i in data:
        if i[-1] is None:
            names.append(i[0])

    details_frame = Frame(main_frame, bg='#f2f3d2')
    details_frame.grid(row=0, column=0)

    names_label = Label(details_frame, text='Name:', bg='#f2f3d2')
    names_label.grid(row=0, column=0)
    names_dropdown = OptionMenu(details_frame, name, *names)
    names_dropdown.grid(row=0, column=1)

    btn_extract = Button(main_frame, text='Extract Data', bd=5, relief=RIDGE, command=extraction)
    btn_extract.grid(row=1, column=0)

    # DISPLAY ALL THE DETAILS OF OWNER AS PER DROPDOWN SELECTION

    final_bill_text = Text(main_frame, bd=5, width=100, height=30, relief=SUNKEN, font=('Helvatica Bold', 12))
    final_bill_text.grid(row=0, column=1)

    btn_print = Button(main_frame, text='Print Bill', bd=5, relief=RIDGE, command=CheckOut)
    btn_print.grid(row=1, column=1)


def def_feedback():

    def display_rating():
        # SAVE THE FEEDBACKS IN A CSV FILE FOR DATASET

        f = open('FeedbackData.csv', 'a')
        f.write("{},{},{}\n".format(food_rating.get(), room_service_rating.get(), overall_rating.get()))
        f.close()

        food_rating.set('0')
        room_service_rating.set('0')
        overall_rating.set('0')

    food_rating_options = [str(i) for i in range(0, 11)]
    room_service_rating_options = [str(i) for i in range(0, 11)]
    overall_rating_options = [str(i) for i in range(0, 11)]

    food_rating = StringVar()
    food_rating.set('0')
    room_service_rating = StringVar()
    room_service_rating.set('0')
    overall_rating = StringVar()
    overall_rating.set('0')

    food_rating_label = Label(main_frame, text='Food Rating:', bg='#f2f3d2')
    food_rating_label.grid(row=0, column=0, padx=5, pady=10)
    room_service_rating_label = Label(main_frame, text='Room Service Rating:', bg='#f2f3d2')
    room_service_rating_label.grid(row=1, column=0, padx=5, pady=10)
    overall_rating_label = Label(main_frame, text='Overall Rating:', bg='#f2f3d2')
    overall_rating_label.grid(row=2, column=0, padx=5, pady=10)

    food_rating_entry = OptionMenu(main_frame, food_rating, *food_rating_options)
    food_rating_entry.grid(row=0, column=1, padx=5, pady=10)
    room_service_rating_entry = OptionMenu(main_frame, room_service_rating, *room_service_rating_options)
    room_service_rating_entry.grid(row=1, column=1, padx=5, pady=10)
    overall_rating_entry = OptionMenu(main_frame, overall_rating, *overall_rating_options)
    overall_rating_entry.grid(row=2, column=1, padx=5, pady=10)

    submit_button = Button(main_frame, text='Submit', bd=5, relief=RIDGE, command=display_rating)
    submit_button.grid(row=3, column=0, columnspan=2)


#Main Frame Functions


def return_home():
    global main_frame, root, main_page, food_facility, records, final_bill, feedback, exit_button
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    # Main Frame Contents
    main_page = Button(main_frame, text='Main Page', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=main_page_func, bg='#a2b3c2')
    main_page.grid(row=0, column=0, pady=10)
    food_facility = Button(main_frame, text='Food Facility', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=food_facility_func, bg='#a2b3c2')
    food_facility.grid(row=1, column=0, pady=10)
    records = Button(main_frame, text='Records', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=records_func, bg='#a2b3c2')
    records.grid(row=2, column=0, pady=10)
    final_bill = Button(main_frame, text='Final Bill', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=final_bill_func, bg='#a2b3c2')
    final_bill.grid(row=3, column=0, pady=10)
    feedback = Button(main_frame, text='Feedback', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=feedback_func, bg='#a2b3c2')
    feedback.grid(row=4, column=0, pady=10)
    exit_button = Button(main_frame, text='Exit', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=root.destroy, bg='#a2b3c2')
    exit_button.grid(row=5, column=0, pady=10)


def main_page_func():
    global main_frame, root, home_page
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    def_main_page()

    home_page = Button(main_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home, font=('Helvatical Bold', 11))
    home_page.grid(sticky=S, padx=5, pady=5, columnspan=2)


def food_facility_func():
    global main_frame, root, home_page, menu_frame, bill_frame, cost_frame, button_frame
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    menu_frame = Frame(main_frame, width=80, height=20, bg='#f2f3d2')
    menu_frame.grid(row=0, column=0)
    bill_frame = Frame(main_frame, bd=5, relief=SUNKEN, width=20, height=10, bg='#d2e3f2')
    bill_frame.grid(row=0, column=1, rowspan=2)
    cost_frame = Frame(main_frame, bd=5, relief=SUNKEN, width=20, height=10, bg='#d2e3f2')
    cost_frame.grid(row=1, column=0)
    button_frame = Frame(main_frame, bd=5, relief=SUNKEN, bg='#d2e3f2')
    button_frame.grid(row=2, column=0)

    def_food_facility()

    home_page = Button(button_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home, font=('Helvatica Bold', 11))
    home_page.grid(row=0, column=3, padx=5, pady=5)


def records_func():
    global main_frame, root, home_page
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    def_records()

    home_page = Button(main_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home)
    home_page.grid(sticky=S, padx=5, pady=5)


def final_bill_func():
    global main_frame, root, home_page
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    def_final_bill()

    home_page = Button(main_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home)
    home_page.grid(row=2, column=1, padx=5, pady=5)


def feedback_func():
    global main_frame, root, home_page
    main_frame.destroy()

    main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
    main_frame.pack()

    def_feedback()

    home_page = Button(main_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home)
    home_page.grid(sticky=S, padx=5, pady=5, columnspan=2)


#----------------------------------------------Creating Main Frame-----------------------------------------------------

single_bed_available_rooms = [101, 201, 301, 401, 501, 601, 701, 801, 901, 1001]
double_bed_available_rooms = [102, 103, 202, 203, 302, 303, 402, 403, 502, 503, 602, 603, 702, 703, 802, 803, 902, 903, 1002, 1003]
triple_bed_available_rooms = [104, 204, 304, 404, 504, 604, 704, 804, 904, 1004]

single_bed_occupied = []
double_bed_occupied = []
triple_bed_occupied = []


dataset = select_op()
if len(dataset) != 0:
    for k in dataset:
        if int(k[3]) in single_bed_available_rooms:
            single_bed_occupied.append(single_bed_available_rooms.pop(single_bed_available_rooms.index(int(k[3]))))

        elif int(k[3]) in double_bed_available_rooms:
            double_bed_occupied.append(double_bed_available_rooms.pop(double_bed_available_rooms.index(int(k[3]))))

        elif int(k[3]) in triple_bed_available_rooms:
            triple_bed_occupied.append(triple_bed_available_rooms.pop(triple_bed_available_rooms.index(int(k[3]))))

hotel_name_label = Label(root, text="Hotel Bliss Fort", bd=8, height=3, relief=RIDGE, font=('Helvatical bold', 20), fg='white', bg='#223344')
hotel_name_label.pack(fill=X, padx=5, pady=20)

main_frame = Frame(root, height=100, width=200, bg='#f2f3d2')
main_frame.pack()

home_page = Button(main_frame, text='Main Menu', bd=5, relief=RIDGE, command=return_home)

#Main Frame Contents
main_page = Button(main_frame, text='Main Page', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=main_page_func, bg='#a2b3c2')
food_facility = Button(main_frame, text='Food Facility', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=food_facility_func, bg='#a2b3c2')
records = Button(main_frame, text='Records', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=records_func, bg='#a2b3c2')
final_bill = Button(main_frame, text='Final Bill', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=final_bill_func, bg='#a2b3c2')
feedback = Button(main_frame, text='Final Bill', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=feedback_func, bg='#a2b3c2')
exit_button = Button(main_frame, text='Exit', bd=5, relief=RIDGE, width=25, height=2, font=('Helvatical Bold', 15), command=root.destroy, bg='#a2b3c2')

return_home()

root.mainloop()
