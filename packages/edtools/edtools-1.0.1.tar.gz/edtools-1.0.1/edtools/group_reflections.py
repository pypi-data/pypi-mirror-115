import numpy as np
import pandas as pd
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from cctbx import crystal, miller
from cctbx.array_family import flex
from iotbx.reflection_file_reader import any_reflection_file


class GroupReflectionsGUI(LabelFrame):
    """A GUI frame for reflections grouping"""
    def __init__(self, parent):
        LabelFrame.__init__(self, parent, text='Grouping reflections')
        self.parent = parent

        self.init_vars()

        frame = Frame(self)

        self.FileButton = Button(frame, text='Select File', width=15, command=self.open_file, state=NORMAL)
        self.FileButton.grid(row=0, column=0, sticky='EW', padx=5)
        self.lb_file = Label(frame, text='')
        self.lb_file.grid(row=0, column=1, sticky='W', padx=5)

        frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)

        frame = Frame(self)

        self.lb_cell = Label(frame, text='Unit Cell')
        self.lb_cell.grid(row=1, column=0, sticky='EW')
        vcmd = (self.parent.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.lb_a = Label(frame, text='a')
        self.lb_a.grid(row=1, column=1, sticky='EW', padx=5)
        self.e_a = Entry(frame, textvariable=self.var_a, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_a.focus()
        self.e_a.grid(row=1, column=2, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=3, sticky='EW')

        self.lb_b = Label(frame, text='b')
        self.lb_b.grid(row=1, column=4, sticky='EW', padx=5)
        self.e_b = Entry(frame, textvariable=self.var_b, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_b.focus()
        self.e_b.grid(row=1, column=5, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=6, sticky='EW')

        self.lb_c = Label(frame, text='c')
        self.lb_c.grid(row=1, column=7, sticky='EW', padx=5)
        self.e_c = Entry(frame, textvariable=self.var_c, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_c.focus()
        self.e_c.grid(row=1, column=8, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=9, sticky='EW')

        self.lb_alpha = Label(frame, text='alpha')
        self.lb_alpha.grid(row=1, column=10, sticky='EW', padx=5)
        self.e_alpha = Entry(frame, textvariable=self.var_alpha, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_alpha.focus()
        self.e_alpha.grid(row=1, column=11, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=12, sticky='EW')

        self.lb_beta = Label(frame, text='beta')
        self.lb_beta.grid(row=1, column=13, sticky='EW', padx=5)
        self.e_beta = Entry(frame, textvariable=self.var_beta, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_beta.focus()
        self.e_beta.grid(row=1, column=14, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=15, sticky='EW')

        self.lb_gamma = Label(frame, text='gamma')
        self.lb_gamma.grid(row=1, column=16, sticky='EW', padx=5)
        self.e_gamma = Entry(frame, textvariable=self.var_gamma, width=5, validate='key', validatecommand=vcmd, state=NORMAL)
        self.e_gamma.focus()
        self.e_gamma.grid(row=1, column=17, sticky='EW')
        Label(frame, text='Å').grid(row=1, column=18, sticky='EW')

        frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)

        frame = Frame(self)

        self.lb_space_group = Label(frame, text='Space Group')
        self.lb_space_group.grid(row=0, column=0, sticky='EW')
        self.e_space_group = Entry(frame, textvariable=self.var_space_group, width=10, state=NORMAL)
        self.e_space_group.grid(row=0, column=1, sticky='EW', padx=5)

        self.lb_save_name = Label(frame, text='Save File')
        self.lb_save_name.grid(row=0, column=2, sticky='EW', padx=5)
        self.e_save_name = Entry(frame, textvariable=self.var_save_name, width=10, state=NORMAL)
        self.e_save_name.grid(row=0, column=3, sticky='EW')
        appendix_options = [".hkl", ".csv"]
        self.e_rotspeed = OptionMenu(frame, self.var_appendix, ".hkl", *appendix_options)
        self.e_rotspeed.grid(row=0, column=4, sticky='W')

        self.lb_ratio = Label(frame, text="Ratio")
        self.lb_ratio.grid(row=0, column=5, sticky='EW', padx=5)
        vcmd_range = (self.parent.register(self.validate_range), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_ratio = Entry(frame, textvariable=self.var_ratio, width=10, validate='key', validatecommand=vcmd_range, state=NORMAL)
        self.e_ratio.grid(row=0, column=6, sticky='EW')

        frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)

        frame = Frame(self)

        Checkbutton(frame, text='Scale Iobs', variable=self.var_scale_iobs, width=8).grid(row=1, column=0, sticky='EW')
        Label(frame, text="Power").grid(row=1, column=1, sticky='EW', padx=5)
        self.e_power = Entry(frame, textvariable=self.var_power, width=10, state=NORMAL)
        self.e_power.grid(row=1, column=2, sticky='EW')
        Checkbutton(frame, text='Save smaller', variable=self.var_save_smaller, width=12).grid(row=1, column=3, sticky='EW', padx=5)

        frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)

        frame = Frame(self)

        self.SaveButton = Button(frame, text='Save Grouped', width=15, command=self.save_grouped, state=NORMAL)
        self.SaveButton.grid(row=0, column=0, sticky='EW', padx=5)
        self.SplitButton = Button(frame, text='Split Grouped', width=15, command=self.split_grouped, state=NORMAL)
        self.SplitButton.grid(row=0, column=1, sticky='EW', padx=5)

        frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)

        

    def init_vars(self):
        self.file_name = ""
        self.var_a = DoubleVar(value=10.0)
        self.var_b = DoubleVar(value=10.0)
        self.var_c = DoubleVar(value=10.0)
        self.var_alpha = DoubleVar(value=90.0)
        self.var_beta = DoubleVar(value=90.0)
        self.var_gamma = DoubleVar(value=90.0)
        self.var_space_group = StringVar(value="")
        self.var_save_name = StringVar(value="")
        self.var_appendix = StringVar(value=".hkl")
        self.var_ratio = DoubleVar(value=0.5)
        self.var_scale_iobs = BooleanVar(value=False)
        self.var_power = DoubleVar(value=4/3)
        self.var_save_smaller = BooleanVar(value=False)


    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                value = float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def validate_range(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                value = float(value_if_allowed)
                if value > 0 and value < 1:
                    return True
                else:
                    return False
            except ValueError:
                return False
        else:
            return False


    def open_file(self):
        self.file_name = filedialog.askopenfilename(initialdir='.', title='Select file', 
                            filetypes=(('hkl files', '*.hkl'), ('all files', '*.*')))
        self.lb_file.config(text=self.file_name)

    def save_file(self, df):
        filetype = self.var_appendix.get()
        if filetype == ".csv":
            df.to_csv(self.var_save_name.get()+self.var_appendix.get())
        elif filetype == ".hkl":
            ms = miller.set(crystal_symmetry=crystal.symmetry(space_group_symbol=self.space_group, unit_cell=self.unit_cell), anomalous_flag=False,
               indices=flex.miller_index(list(df['indice'])))
            ma = miller.array(ms, data=flex.double(list(df['I'].map(lambda x: round(x,2)))), 
                  sigmas=flex.double(list(df['sigma'].map(lambda x: round(x,2)))))
            with open(self.var_save_name.get()+filetype, 'w') as f:
                ma.export_as_shelx_hklf(f)

    def group_df(self):
        self.unit_cell = (self.var_a.get(), self.var_b.get(), self.var_c.get(), self.var_alpha.get(), self.var_beta.get(), self.var_gamma.get())
        self.space_group = self.var_space_group.get()
        hkl = any_reflection_file(f"{self.file_name}=hklf4").as_miller_arrays(crystal.symmetry(unit_cell=self.unit_cell, space_group_symbol=self.space_group))[0]
        merge_eq_hkl = hkl.merge_equivalents().array()
        merge_eq_hkl_indice = pd.DataFrame(merge_eq_hkl,columns=('indice2', 'I', 'sigma'))

        df = pd.DataFrame(merge_eq_hkl.expand_to_p1(),columns=('indice1','I','sigma')).merge(merge_eq_hkl_indice,left_on='indice1',right_on='indice2',how='left')[['indice1','indice2']]
        df = df.fillna(method='ffill')
        df_fpair = pd.DataFrame(df['indice1'].apply(lambda x:(-x[0],-x[1],-x[2])))
        df_fpair['indice2'] = df['indice2']
        df = df.append(df_fpair)

        hkl_df = pd.DataFrame(hkl,columns=('indice','I','sigma'))
        hkl_df_no_dup = hkl_df.groupby('indice').mean().reset_index()

        merged = hkl_df_no_dup.merge(df,left_on='indice',right_on='indice1',how='left')
        merged = merged.sort_values('indice2').drop(['indice1'], axis=1)

        return merged

    def scaling_factor(self, value, power):
        if value > 0:
            result =  value ** power
        else:
            result = (-value) ** power
            result = - result
        return result

    def scaling_func(self, value, power):
        if value > 0:
            result = (1 + value) ** power
        else:
            result  = -(1 - value) ** power
        return result

    def save_grouped(self):
        merged = self.group_df()
        self.save_file(merged)

    def split_grouped(self):
        merged = self.group_df()

        merged_g = merged.groupby(['indice2'], group_keys=False)
        merged_g_sorted = merged_g.apply(pd.DataFrame.sort_values, ['I'])

        selected_g_larger = merged_g_sorted.groupby('indice2', group_keys=False).apply(lambda x: x.iloc[int(x.I.size*self.var_ratio.get()):])
        selected_g_smaller = merged_g_sorted.groupby('indice2', group_keys=False).apply(lambda x: x.iloc[:int(x.I.size*self.var_ratio.get())])

        if self.var_scale_iobs.get():
            power = self.var_power.get()
            #selected_g_larger['I'] = selected_g_larger['I'] / 400
            #selected_g_larger['sigma'] = selected_g_larger['sigma'] / 400

            selected_g_larger['sigma'] = selected_g_larger['sigma'] * selected_g_larger['I'].apply(lambda x: power*self.scaling_func(x, power-1))
            selected_g_larger['I'] = selected_g_larger['I'].apply(lambda x: self.scaling_func(x, power)) * selected_g_larger['I']
            
        if self.var_save_smaller.get():
            self.save_file(selected_g_smaller)
        else:
            self.save_file(selected_g_larger)

def main():
    root = Tk()
    GroupReflectionsGUI(root).pack(side='top', fill='both', expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()
