import customtkinter
import os
from PIL import Image
import Models

class App(customtkinter.CTk):

    def __init__(self):

        # On-Click Button Function
        # For Queuing
        def MMCQ():
            try:
                lambd = float(lamdb_mmcq.get())
                mu = float(mu_mmcq.get())
                c = int(nos_mmcq.get())

                Lq, Wq, Ws, Ls, utilization, po = Models.mmc_queue(lambd, mu, c)
                result_box.delete("1.0", "end")
                result_data = [
                    ["Length of a Queue :  " + str(Lq), "", "Length of a System :  " + str(Ls)],
                    ["Waiting in a Queue :  " + str(Wq), "", "Waiting in a System :  " + str(Ws)],
                    ["Utilization :  " + str(utilization), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    result_box.insert("end", formatted_row)

                if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or po < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")
            except:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "There is some error in the data you entered!")

        def MGCQ():
            try:
                lambd = float(lamdb_mgcq.get())
                general_distribution = str(general_distribution_mgcq.get())
                min_mean_shape = float(min_mean_shape_mgcq.get())
                max_var_scale = float(max_var_scale_mgcq.get())
                c = int(nos_mgcq.get())

                Lq, Wq, Ws, Ls, utilization = Models.mgc_queue(lambd, c, general_distribution, min_mean_shape, max_var_scale)
                result_box.delete("1.0", "end")
                result_data = [
                    ["Length of a Queue :  " + str(Lq), "", "Length of a System :  " + str(Ls)],
                    ["Waiting in a Queue :  " + str(Wq), "", "Waiting in a System :  " + str(Ws)],
                    ["Utilization :  " + str(utilization), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    result_box.insert("end", formatted_row)

                if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")
            except:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "There is some error in the data you entered!")

        def GGCQ():
            try:
                arrival_dist = str(arrival_dist_ggc.get())
                service_dist = str(service_dist_ggc.get())
                min_mean_shape_arivl = float(min_mean_shape_arvl.get())
                min_mean_shape_srvic = float(min_mean_shape_srvc.get())
                max_var_scale_arivl = float(max_var_scale_arvl.get())
                max_var_scale_srvic = float(max_var_scale_srvc.get())
                c = int(nos_ggc.get())

                Lq, Wq, Ws, Ls, utilization = Models.ggc_queue(arrival_dist, service_dist, min_mean_shape_arivl, min_mean_shape_srvic, max_var_scale_arivl, max_var_scale_srvic, c)
                result_box.delete("1.0", "end")
                result_data = [
                    ["Length of a Queue :  " + str(Lq), "", "Length of a System :  " + str(Ls)],
                    ["Waiting in a Queue :  " + str(Wq), "", "Waiting in a System :  " + str(Ws)],
                    ["Utilization :  " + str(utilization), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    result_box.insert("end", formatted_row)

                if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")
            except:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "There is some error in the data you entered!")


        # For Simulation
        def MMCS():
            try:
                arrival = float(arrival_rate.get())
                service = float(service_rate.get())
                nos = int(nos_mmcs.get())
                spreadsheet = chk_box_mmcs.get()
                priority = priority_mmcs.get()
                avg_arrival, avg_service, Ta, Wt, Res = Models.mmc_simulation(arrival, service, nos, spreadsheet, priority)
                res_box.delete("1.0", "end")
                result_data = [
                    ["Avg. Arrival Time :  " + str(avg_arrival), " ", " Avg. Service Time :  " + str(avg_service)],
                    ["Avg. Turn-Around :  " + str(Ta), "", "Avg. Wait Time :  " + str(Wt)],
                    ["Response :  " + str(Res), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    res_box.insert("end", formatted_row)

                '''if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")'''

            except:
                res_box.delete("1.0", "end")
                res_box.insert("1.0", "There is some error in the data you entered!")

        def MGCS():
            try:
                arrival = float(arrival_mgcs.get())
                general_distribution = str(gen_dist_mgcs.get())
                min_mean_shape = float(min_mean_shape_mgcs.get())
                max_var_scale = float(max_var_scale_mgcs.get())
                spreadsheet = chk_box_mgcs.get()
                nos = int(nos_mgcs.get())
                priority = priority_mgcs.get()
                avg_arrival, avg_service, Ta, Wt, Res = Models.mgc_simulation(arrival, general_distribution, min_mean_shape, max_var_scale, nos, spreadsheet, priority)
                res_box.delete("1.0", "end")
                result_data = [
                    ["Avg. Arrival Time :  " + str(avg_arrival), " ", " Avg. Service Time :  " + str(avg_service)],
                    ["Avg. Turn-Around :  " + str(Ta), "", "Avg. Wait Time :  " + str(Wt)],
                    ["Response :  " + str(Res), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    res_box.insert("end", formatted_row)

                '''if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")'''

            except:
                res_box.delete("1.0", "end")
                res_box.insert("1.0", "There is some error in the data you entered!")

        def GGCS():
            try:
                arrival_distribution = str(arrival_distribution_ggcs.get())
                service_distribution = str(service_distribution_ggcs.get())
                min_mean_shape_arvl = float(min_mean_shape_arvl_ggcs.get())
                min_mean_shape_srvc = float(min_mean_shape_srvc_ggcs.get())
                max_var_scale_arvl = float(max_var_scale_arvl_ggcs.get())
                max_var_scale_srvc = float(max_var_scale_srvc_ggcs.get())
                spreadsheet = chk_box_ggcs.get()
                nos = int(nos_ggcs.get())
                priority = priority_ggcs.get()
                avg_arrival, avg_service, Ta, Wt, Res = Models.ggc_simulation(arrival_distribution, service_distribution, min_mean_shape_arvl, min_mean_shape_srvc, max_var_scale_arvl, max_var_scale_srvc, nos, spreadsheet, priority)
                res_box.delete("1.0", "end")
                result_data = [
                    ["Avg. Arrival Time :  " + str(avg_arrival), " ", " Avg. Service Time :  " + str(avg_service)],
                    ["Avg. Turn-Around :  " + str(Ta), "", "Avg. Wait Time :  " + str(Wt)],
                    ["Response :  " + str(Res), "", ""]
                ]
                # Insert formatted data into the text box
                for row in result_data:
                    formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
                    res_box.insert("end", formatted_row)

                '''if Lq < 0 or Wq < 0 or Ws < 0 or Ls < 0 or utilization < 0 or utilization > 1:
                    result_box.insert("4.0", "There is some error in the data you entered!")'''

            except:
                res_box.delete("1.0", "end")
                res_box.insert("1.0", "There is some error in the data you entered!")


        super().__init__()
        self.title("Queue Master")
        self.geometry("690x530")
        self.maxsize(width=690, height=530)
        self.minsize(width=690, height=530)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.simulation = customtkinter.CTkImage(Image.open(os.path.join(image_path, "simulation.png")), size=(500, 135))
        self.queueing_model = customtkinter.CTkImage(Image.open(os.path.join(image_path, "queueing_model.png")), size=(500, 135))
        self.mmc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "mmc.png")), size=(500, 135))
        self.mgc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "mgc.png")), size=(500, 135))
        self.ggc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ggc.png")), size=(500, 135))

        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calculator.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "calculator.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calculator.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "calculator.png")), size=(20, 20))
        #self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calculator.png")), dark_image=Image.open(os.path.join(image_path, "calculator.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Queue Master", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40, border_spacing=10, text="Simulation",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40, border_spacing=10, text="Queueing Model",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        '''
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40, border_spacing=10, text="G/G/C",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        '''
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=4, column=0, padx=25, pady=24, sticky="s")

        # CREATING HOME NAV_OPTION
        # FOR SIMULATION

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=0)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.simulation)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=0, pady=0)

        # Frame 1
        frame_1 = customtkinter.CTkFrame(master=self.home_frame, width=450, height=150)
        frame_1.grid(row=1, column=0, pady=(0,5), padx=5)

        res_box = customtkinter.CTkTextbox(master=frame_1, width=450, height=75)
        res_box.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="w")
        result_data = [
            ["Avg. Arrival Time :  " + "0000", " ", " Avg. Service Time :  " + "0000"],
            ["Avg. Turn-Around :  " + "0000", "", "Avg. Wait Time :  " + "0000"],
            ["Response :  " + "0000", "", ""]
        ]
        # Insert formatted data into the text box
        for row in result_data:
            formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
            res_box.insert("end", formatted_row)

        self.tabview = customtkinter.CTkTabview(self.home_frame, width=450, height=240)
        self.tabview.grid(row=2, column=0, padx=10, pady=0)
        self.tabview.add("M/M/C")
        self.tabview.add("M/G/C")
        self.tabview.add("G/G/C")
        self.tabview.tab("M/M/C").grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("M/G/C").grid_columnconfigure(0, weight=0)
        self.tabview.tab("G/G/C").grid_columnconfigure(0, weight=0)

        # FOR SIMULATION
        # Tabview # 1
        # For M/M/C
        arrival_rate = customtkinter.CTkEntry(self.tabview.tab("M/M/C"), width=440, height=35, placeholder_text="Rate Of Arrival (λ)")
        arrival_rate.grid(row=1, column=0, columnspan="2", pady=6, padx=10, sticky="we")

        service_rate = customtkinter.CTkEntry(self.tabview.tab("M/M/C"), width=200, height=35, placeholder_text="Rate Of Service (μ)")
        service_rate.grid(row=2, column=0, columnspan="2", pady=6, padx=10, sticky="we")

        # Dropdown in Frame 1
        nos_mmcs = customtkinter.CTkComboBox(self.tabview.tab("M/M/C"), width=200, height=35, values=["1", "2", "3", "4", "5"])
        nos_mmcs.grid(row=3, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        nos_mmcs.set("No. of Servers")

        chkbox_frame = customtkinter.CTkFrame(self.tabview.tab("M/M/C"), width=210, height=35)
        chkbox_frame.grid(row=4, column=0, pady=6, padx=10, sticky="we")
        priority_mmcs = customtkinter.CTkCheckBox(master=chkbox_frame, text="Generate Priority")
        priority_mmcs.grid(row=0, column=0, pady=6, padx=10)

        checkbox_frame = customtkinter.CTkFrame(self.tabview.tab("M/M/C"), width=210, height=35)
        checkbox_frame.grid(row=4, column=1, pady=6, padx=10, sticky="we")
        chk_box_mmcs = customtkinter.CTkCheckBox(master=checkbox_frame, text="Generate Spreadsheet")
        chk_box_mmcs.grid(row=0, column=0, pady=6, padx=10)

        btn_mmcs = customtkinter.CTkButton(self.tabview.tab("M/M/C"), width=200, height=35, command=MMCS)
        btn_mmcs.grid(row=5, column=0, columnspan=2, pady=6, padx=10, sticky="we")
        btn_mmcs.configure(text="Generate Result")

        # Tabview # 2
        # For M/G/C
        arrival_mgcs= customtkinter.CTkEntry(self.tabview.tab("M/G/C"), width=210, height=35, placeholder_text="Rate Of Arrival (λ)")
        arrival_mgcs.grid(row=1, column=0, pady=6, padx=10)

        gen_dist_mgcs = customtkinter.CTkComboBox(self.tabview.tab("M/G/C"), width=210, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        gen_dist_mgcs.grid(row=1, column=1, pady=6, padx=10,)
        gen_dist_mgcs.set("General Distribution")

        min_mean_shape_mgcs = customtkinter.CTkEntry(self.tabview.tab("M/G/C"), placeholder_text="Min/Mean/Shape", width=210, height=35)
        min_mean_shape_mgcs.grid(row=2, column=0, pady=6, padx=10)

        max_var_scale_mgcs = customtkinter.CTkEntry(self.tabview.tab("M/G/C"), placeholder_text="Max/Variance/Scale", width=210, height=35)
        max_var_scale_mgcs.grid(row=2, column=1, pady=6, padx=10)

        nos_mgcs = customtkinter.CTkComboBox(self.tabview.tab("M/G/C"), width=200, height=35, values=["1", "2", "3", "4", "5"])
        nos_mgcs.grid(row=3, column=0, pady=6, padx=10, columnspan="2", sticky="we")
        nos_mgcs.set("No. of Servers")

        checkbox_frame = customtkinter.CTkFrame(master=self.tabview.tab("M/G/C"), width=200, height=35)
        checkbox_frame.grid(row=4, column=0, pady=6, padx=10, sticky="we")
        priority_mgcs = customtkinter.CTkCheckBox(master=checkbox_frame, text="Generate Priority")
        priority_mgcs.grid(row=1, column=0, pady=6, padx=10)

        chkbox_frame = customtkinter.CTkFrame(master=self.tabview.tab("M/G/C"), width=200, height=35)
        chkbox_frame.grid(row=4, column=1, pady=6, padx=10, sticky="we")
        chk_box_mgcs = customtkinter.CTkCheckBox(master=chkbox_frame, text="Generate Spreadsheet")
        chk_box_mgcs.grid(row=1, column=0, pady=6, padx=10)

        btn_mgcs = customtkinter.CTkButton(self.tabview.tab("M/G/C"), width=200, height=35, command=MGCS)
        btn_mgcs.grid(row=5, column=0, columnspan=2, pady=6, padx=10, sticky="we")
        btn_mgcs.configure(text="Generate Result")

        # Tabview # 3
        # For G/G/C
        arrival_distribution_ggcs = customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=210, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        arrival_distribution_ggcs.grid(row=2, column=0, pady=6, padx=10)
        arrival_distribution_ggcs.set("General Dist. (For Arrival)")

        service_distribution_ggcs= customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=210, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        service_distribution_ggcs.grid(row=2, column=1, pady=6, padx=10)
        service_distribution_ggcs.set("General Dist. (For Service)")

        min_mean_shape_arvl_ggcs = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Min/Mean/Shape (Arrival)", width=210, height=35)
        min_mean_shape_arvl_ggcs.grid(row=3, column=0, pady=6, padx=10)

        min_mean_shape_srvc_ggcs = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Min/Mean/Shape (Service)", width=210, height=35)
        min_mean_shape_srvc_ggcs.grid(row=3, column=1, pady=6, padx=10)

        max_var_scale_arvl_ggcs = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Max/Variance/Scale (Arrival)", width=210, height=35)
        max_var_scale_arvl_ggcs.grid(row=4, column=0, pady=6, padx=10)

        max_var_scale_srvc_ggcs = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Max/Variance/Scale (Service)", width=210, height=35)
        max_var_scale_srvc_ggcs.grid(row=4, column=1, pady=6, padx=10)

        nos_ggcs = customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=210, height=35, values=["1", "2", "3", "4", "5"])
        nos_ggcs.grid(row=5, column=0, pady=6, padx=10)
        nos_ggcs.set("No. of Servers")

        chkbox_frame = customtkinter.CTkFrame(master=self.tabview.tab("G/G/C"), width=210, height=35)
        chkbox_frame.grid(row=5, column=1, pady=6, padx=10, sticky="we")
        priority_ggcs = customtkinter.CTkCheckBox(master=chkbox_frame, text="Generate Priority")
        priority_ggcs.grid(row=1, column=0, pady=6, padx=10, sticky="we")

        checkbox_frame = customtkinter.CTkFrame(master=self.tabview.tab("G/G/C"), width=210, height=35)
        checkbox_frame.grid(row=6, column=0, pady=6, padx=10, sticky="we")
        chk_box_ggcs = customtkinter.CTkCheckBox(master=checkbox_frame, text="Generate Spreadsheet")
        chk_box_ggcs.grid(row=1, column=0, pady=6, padx=10, sticky="we")

        btn_ggcs = customtkinter.CTkButton(self.tabview.tab("G/G/C"), width=210, height=35, command=GGCS)
        btn_ggcs.grid(row=6, column=1, pady=6, padx=10, sticky="we")
        btn_ggcs.configure(text="Generate Result")

        # CREATING SECOND NAV_OPTION
        # FOR QUEUEING MODEL
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=0)

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.queueing_model)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=0, pady=0)

        # Frame 1
        frame_1 = customtkinter.CTkFrame(master=self.second_frame, width=450, height=320)
        frame_1.grid(row=1, column=0, pady=(0,5), padx=5)

        result_box = customtkinter.CTkTextbox(master=frame_1, width=450, height=75)
        result_box.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="we")
        result_data = [
            ["Length of a Queue :  " + "0000", " ", "Length of a System :  " + "0000"],
            ["Waiting in System :  " + "0000", "", " Waiting in System :  " + "0000"],
            ["Utilization :  " + "0000", "", ""]
        ]
        # Insert formatted data into the text box
        for row in result_data:
            formatted_row = "{:<15} {:<15} {:<15}\n".format(*row)
            result_box.insert("end", formatted_row)

        self.tabview = customtkinter.CTkTabview(self.second_frame, width=450, height=240)
        self.tabview.grid(row=2, column=0, padx=10, pady=0)
        self.tabview.add("M/M/C")
        self.tabview.add("M/G/C")
        self.tabview.add("G/G/C")
        self.tabview.tab("M/M/C").grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("M/G/C").grid_columnconfigure(0, weight=0)
        self.tabview.tab("G/G/C").grid_columnconfigure(0, weight=0)

        # Queuing Model
        # Tabview # 1
        # For M/M/C
        lamdb_mmcq = customtkinter.CTkEntry(self.tabview.tab("M/M/C"), width=440, height=35, placeholder_text="Rate Of Arrival (λ) (In Minutes)")
        lamdb_mmcq.grid(row=1, column=0, columnspan="2", pady=6, padx=10, sticky="we")

        mu_mmcq = customtkinter.CTkEntry(self.tabview.tab("M/M/C"), width=200, height=35, placeholder_text="Rate Of Service (μ) (In Minutes)")
        mu_mmcq.grid(row=2, column=0, columnspan="2", pady=6, padx=10, sticky="we")

        nos_mmcq = customtkinter.CTkComboBox(self.tabview.tab("M/M/C"), width=200, height=35,
                                               values=["1", "2", "3", "4", "5"])
        nos_mmcq.grid(row=3, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        nos_mmcq.set("No. of Servers")

        rand_mmcq = customtkinter.CTkEntry(self.tabview.tab("M/M/C"), placeholder_text="Random Numbers (Not Required)", width=200, height=35)
        rand_mmcq.grid(row=4, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        rand_mmcq.configure(state="disabled")

        btn_mmcq = customtkinter.CTkButton(self.tabview.tab("M/M/C"), width=200, height=35, command=MMCQ)
        btn_mmcq.grid(row=5, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        btn_mmcq.configure(text="Generate Result")

        # Tabview # 2
        # For M/G/C
        lamdb_mgcq = customtkinter.CTkEntry(self.tabview.tab("M/G/C"), width=440, height=35, placeholder_text="Rate Of Arrival (λ) (In Minutes)")
        lamdb_mgcq.grid(row=2, column=0, pady=6, padx=10, columnspan="2", sticky="we")

        general_distribution_mgcq = customtkinter.CTkComboBox(self.tabview.tab("M/G/C"), width=200, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        general_distribution_mgcq.grid(row=3, column=0, pady=6, padx=10, columnspan="2", sticky="we")
        general_distribution_mgcq.set("General Distribution")

        min_mean_shape_mgcq = customtkinter.CTkEntry(self.tabview.tab("M/G/C"), placeholder_text="Min/Mean/Shape", width=210, height=35)
        min_mean_shape_mgcq.grid(row=4, column=0, pady=6, padx=10)

        max_var_scale_mgcq = customtkinter.CTkEntry(self.tabview.tab("M/G/C"), placeholder_text="Max/Variance/Scale", width=210, height=35)
        max_var_scale_mgcq.grid(row=4, column=1, pady=6, padx=10)

        nos_mgcq = customtkinter.CTkComboBox(self.tabview.tab("M/G/C"), width=200, height=35, values=["1", "2", "3", "4", "5"])
        nos_mgcq.grid(row=5, column=0, pady=6, padx=10, columnspan="2", sticky="we")
        nos_mgcq.set("No. of Servers")

        btn_mgcq = customtkinter.CTkButton(self.tabview.tab("M/G/C"), width=200, height=35, command=MGCQ)
        btn_mgcq.grid(row=6, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        btn_mgcq.configure(text="Generate Result")

        # Tabview # 3
        # For G/G/C
        arrival_dist_ggc = customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=210, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        arrival_dist_ggc.grid(row=2, column=0, pady=6, padx=10)
        arrival_dist_ggc.set("General Dist. (For Arrival)")

        service_dist_ggc = customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=210, height=35,
                                               values=["Normal Distribution", "Uniform Distribution",
                                                       "Gamma Distribution"])
        service_dist_ggc.grid(row=2, column=1, pady=6, padx=10)
        service_dist_ggc.set("General Dist. (For Service)")

        min_mean_shape_arvl = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Min/Mean/Shape (Arrival)", width=210, height=35)
        min_mean_shape_arvl.grid(row=3, column=0, pady=6, padx=10)

        min_mean_shape_srvc = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Min/Mean/Shape (Service)", width=210, height=35)
        min_mean_shape_srvc.grid(row=3, column=1, pady=6, padx=10)

        max_var_scale_arvl = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Max/Variance/Scale (Arrival)", width=210, height=35)
        max_var_scale_arvl.grid(row=4, column=0, pady=6, padx=10)

        max_var_scale_srvc = customtkinter.CTkEntry(self.tabview.tab("G/G/C"), placeholder_text="Max/Variance/Scale (Service)", width=210, height=35)
        max_var_scale_srvc.grid(row=4, column=1, pady=6, padx=10)

        nos_ggc = customtkinter.CTkComboBox(self.tabview.tab("G/G/C"), width=200, height=35, values=["1", "2", "3", "4", "5"])
        nos_ggc.grid(row=5, column=0, pady=6, padx=10, columnspan="2", sticky="we")
        nos_ggc.set("No. of Servers")

        btn_ggc = customtkinter.CTkButton(self.tabview.tab("G/G/C"), width=200, height=35, command=GGCQ)
        btn_ggc.grid(row=6, column=0, columnspan="2", pady=6, padx=10, sticky="we")
        btn_ggc.configure(text="Generate Result")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        '''    
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        '''

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    '''
    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
    '''
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

