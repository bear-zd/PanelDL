from PanelDL.modoule import PanelDL

if __name__ == '__main__':
    PD = PanelDL()
    PD.login("root","root")
    PD.init(run_name="TEST3")
    PD.log({"train_acc":0.94,"val_acc":0.23})
    PD.log({"train_acc": 0.94, "val_acc": 0.23})
