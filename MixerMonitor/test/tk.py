
import tkinter as tk

class MonitorWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MixerMonitor")
        self.window.geometry("400x300")
        self.entryList = self.setWindow()
        self.running = False
        # --------------------------
        self.update()
        self.window.mainloop()
    # -------------------------------------------------------------------------------------------
    def setWindow(self):
        PLC_DATA = ['PrgNo','BondName','LotNo','RPM','TimeSet','TimeAct']
        entryList = []

        for idx,dataName in enumerate(PLC_DATA):
            label = tk.Label(self.window, text=dataName)
            label.grid(row=idx, column=0, padx=5, pady=5)

            entry = tk.Entry(self.window)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entryList.append(entry)
        return entryList
    # -------------------------------------------------------------------------------------------
    def startUpdate(self):
        self.running = True

    def stopUpdate(self):
        self.running = False

    def updateEntries(self, resList):
        for entry, res in zip(self.entryList, resList):
            entry.delete(0, tk.END)
            entry.insert(0, res)

    def update(self):
        if self.running:
            resList = updateResList() # 클래스 외부 함수에서 업데이트
            self.updateEntries(resList)
        # running값 업데이트
        self.window.after(1000, self.update)

# ===========================================================================================

if __name__ == "__main__":
    app = MonitorWindow()
    
