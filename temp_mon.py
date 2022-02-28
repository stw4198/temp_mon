import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

Tol_bright = ['#4477AA','#66CCEE','#228833',
                     '#CCBB44','#EE6677','#AA3377','#BBBBBB','k']

class Temp_Logs():

	def __init__(self,filename=None,run_date=None,run_time=None,run_length=None):
		self.filename = filename
		self.run_date = run_date
		self.run_time = run_time
		self.run_length = run_length
		
	def parse_options(self,argv=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("filename", help="temperature log to read and plot", type=str)
		parser.add_argument("--run_date", help="date of run (yyyy-mm-dd)", type=str)
		parser.add_argument("--run_time", help="time of run (hh:mm:ss)", type=str)
		parser.add_argument("--run_length", help="length of run (hh:mm:ss)", type=str, default="00:15:00")
		args = parser.parse_args(argv)
		self.filename = args.filename
		self.run_date = args.run_date
		self.run_time = args.run_time
		self.run_length = args.run_length

	def import_data(self):
		stamp,n,t0,t0_err,t1,t1_err,t2,t2_err,t3,t3_err,t4,t4_err,t5,t5_err,t6,t6_err,t7,t7_err,rpre,rpre_err,tpre,tpre_err,rpost,rpost_err,tpost,tpost_err,comment = np.genfromtxt(self.filename,dtype=str,unpack=True,delimiter='\t')

		n = n.astype(np.float)
		t0 = t0.astype(np.float)
		t0_err = t0_err.astype(np.float)
		t1 = t1.astype(np.float)
		t1_err = t1_err.astype(np.float)
		t2 = t2.astype(np.float)
		t2_err = t2_err.astype(np.float)
		t3 = t3.astype(np.float)
		t3_err = t3_err.astype(np.float)
		t4 = t4.astype(np.float)
		t4_err = t4_err.astype(np.float)
		t5 = t5.astype(np.float)
		t5_err = t5_err.astype(np.float)
		t6 = t6.astype(np.float)
		t6_err = t6_err.astype(np.float)
		t7 = t7.astype(np.float)
		t7_err = t7_err.astype(np.float)
		rpre = rpre.astype(np.float)
		rpre_err = rpre_err.astype(np.float)
		tpre = tpre.astype(np.float)
		tpre_err = tpre_err.astype(np.float)
		rpost = rpost.astype(np.float)
		rpost_err = rpost_err.astype(np.float)
		tpost = tpost.astype(np.float)
		tpost_err = tpost_err.astype(np.float)

		date = []
		time = []

		for i in range(len(stamp)):
		  num = 10
		  line = stamp[i]
		  split = [line[i:i+num] for i in range(0, len(line), num)]
		  date.append(split[0])
		  Time = split[1]
		  time.append(Time[1:])
		  
		temp = [t0,t1,t2,t3,t4,t5,t6,t7,tpre,tpost]
		temp_err = [t0_err,t1_err,t2_err,t3_err,t4_err,t5_err,t6_err,t7_err,tpre_err,tpost_err]
		res = [rpre,rpost]
		res_err = [rpre_err,rpost_err]
		
		return(date,time,n,temp,temp_err,res,res_err)
		
	def run_data(self,date,time,n,temp,temp_err):
		t0,t1,t2,t3,t4,t5,t6,t7,tpre,tpost = temp
		t0_err,t1_err,t2_err,t3_err,t4_err,t5_err,t6_err,t7_err,tpre_err,tpost_err = temp_err
		try:		
			hrs,mins,secs = self.run_time.split(":")
			runtime = datetime.time(int(hrs),int(mins),int(secs))
			
			year,month,day = self.run_date.split("-")
			rundate = datetime.date(int(year),int(month),int(day))

			hrs_l,mins_l,secs_l = self.run_length.split(":")
			runlength = datetime.time(int(hrs_l),int(mins_l),int(secs_l))

			length = datetime.datetime.combine(rundate,runlength)
			end = datetime.datetime.combine(rundate,runtime)
			td = end - length
			dt = datetime.datetime.strptime("{} {}".format(rundate, td), "%Y-%m-%d %H:%M:%S")
			run_idx = []
			
			for i in range(len(time)):
				Hrs,Mins,Secs = time[i].split(":")
				Time = datetime.time(int(Hrs),int(Mins),int(Secs))
				Year,Month,Day = date[i].split("-")
				RunDate = datetime.date(int(Year),int(Month),int(Day))
				Run = datetime.datetime.combine(RunDate,Time)
				if Run <= end and Run >= dt:
					run_idx.append(i)
					
			t0_av = np.mean(t0[run_idx])
			t1_av = np.mean(t1[run_idx])
			t2_av = np.mean(t2[run_idx])
			t3_av = np.mean(t3[run_idx])
			t4_av = np.mean(t4[run_idx])
			t5_av = np.mean(t5[run_idx])
			t6_av = np.mean(t6[run_idx])
			t7_av = np.mean(t7[run_idx])
			t_av = np.mean(np.array([t1_av,t2_av,t3_av,t4_av,t6_av]))
			t_av_err = np.std(np.array([t1_av,t2_av,t3_av,t4_av,t6_av]))
			print("Average temperature = %.4f +/- %.4f degC" % (t_av,t_av_err))
		except:
			print("\nCould not calculate average temperature\n")
		return
	
	def plot_data(self,date,time,n,temp,temp_err,res,res_err):
		t0,t1,t2,t3,t4,t5,t6,t7,tpre,tpost = temp
		t0_err,t1_err,t2_err,t3_err,t4_err,t5_err,t6_err,t7_err,tpre_err,tpost_err = temp_err
		rpre,rpost = res
		rpre_err,rpost_err = res_err

		vals = np.arange(0,len(t0))
		
		time_idx = np.round(np.linspace(0, len(time) - 1, 10)).astype(int)

		time_lab = []
		for i in time_idx:
		  time_lab.append(time[i])
		
		new_date = []
		new_date_idx = []
		
		new_date.append(date[0])
		new_date_idx.append(0)
		for i in range(1,len(date)):
			if date[i] != date[i-1]:
				new_date.append(date[i])
				new_date_idx.append(i)

		for i in range(1,len(new_date)):
			colour = str(0. + i/len(new_date))
			plt.axvspan(new_date_idx[i-1], new_date_idx[i], facecolor=colour, alpha=0.5)
		for i in range(len(new_date)):
			plt.text(new_date_idx[i],max(max(t0),max(t1),max(t2),max(t3),max(t4),max(t5),max(t6),max(t7))+0.05,new_date[i])
		plt.errorbar(vals,t0,yerr=t0_err,color=Tol_bright[0],label='t0')
		plt.errorbar(vals,t1,yerr=t1_err,color=Tol_bright[1],label='t1')
		plt.errorbar(vals,t2,yerr=t2_err,color=Tol_bright[2],label='t2')
		plt.errorbar(vals,t3,yerr=t3_err,color=Tol_bright[3],label='t3')
		plt.errorbar(vals,t4,yerr=t4_err,color=Tol_bright[4],label='t4')
		plt.errorbar(vals,t5,yerr=t5_err,color=Tol_bright[5],label='t5 (ambient)')
		plt.errorbar(vals,t6,yerr=t6_err,color='#FFA500',label='t6')
		plt.errorbar(vals,t7,yerr=t7_err,color=Tol_bright[7],label='t7')
		plt.errorbar(vals,tpre,yerr=tpre_err,label='tpre')
		plt.errorbar(vals,tpost,yerr=tpost_err,label='tpost')
		plt.xticks(vals[time_idx],time_lab,rotation=90)
		plt.ylim(5,20)
		plt.legend()
		plt.title("%s - %s (yyyy,mm,dd)" % (date[0],date[-1]))
		plt.ylabel("Temperature [$^o$C]")
		plt.xlabel("Time [24 h]")
		plt.show()

		for i in range(1,len(new_date)):
			colour = str(0. + i/len(new_date))
			plt.axvspan(new_date_idx[i-1], new_date_idx[i], facecolor=colour, alpha=0.5)
		for i in range(len(new_date)):
			plt.text(new_date_idx[i],max(max(rpre),max(rpost))+0.05,new_date[i])
		plt.errorbar(vals,rpre,yerr=rpre_err,label='rpre')
		plt.errorbar(vals,rpost,yerr=rpost_err,label='rpost')
		plt.xticks(vals[time_idx],time_lab,rotation=90)
		#plt.ylim(5,20)
		plt.legend()
		plt.title("%s - %s (yyyy,mm,dd)" % (date[0],date[-1]))
		plt.ylabel("Water Resistivity [MOhm cm]")
		plt.xlabel("Time [24 h]")
		plt.grid()
		plt.show()
		
		return

if __name__ == "__main__":
	temp_logs = Temp_Logs()
	temp_logs.parse_options()
	date,time,n,temp,temp_err,res,res_err = temp_logs.import_data()
	temp_logs.plot_data(date,time,n,temp,temp_err,res,res_err)
	temp_logs.run_data(date,time,n,temp,temp_err)
	
#date,time,n,temp,temp_err = import_data("templog_chiller_17_5_to_15deg.txt")
#plot_data(date,time,n,temp,temp_err)
