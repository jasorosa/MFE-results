import math
import time
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy
import csv


folder = "./results/"
myfile = open("results-analysis.csv",'r')
scurve_data =myfile.read().split('\n')
for i in range(2,130):
	scurve_data[i] = scurve_data[i].split(',')
	for j in range(len(scurve_data[i])):
		scurve_data[i][j] = int(scurve_data[i][j])
scurve_data[1] = scurve_data[1].split(',')
for i in range(1,len(scurve_data[1])):
	scurve_data[1][i] = int(scurve_data[1][i])
	
    
timestamp = time.strftime("%d.%m.%Y %H:%M")
full_data = []
mean_list = []
rms_list = []
full_data.append([""])
full_data.append(["Differential data"])
full_data.append(["", "255-CAL_DAC"])
full_data.append(["Channel", 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, "mean", "RMS"])
dac_values = scurve_data[1][1:]

fig = plt.figure(figsize=(10, 20))
sub1 = plt.subplot(411)

for i in range(2, 130):
	diff = []

	mean_calc = 0
	summ = 0
	data = scurve_data[i][1:]
	channel = scurve_data[i][0]
	l = 0
	diff.append(channel)
	diff.append("")
	for j in data:
		if l != 0:
			diff_value = j - previous_value
			diff.append(diff_value)
			mean_calc += dac_values[l] * diff_value
			summ += diff_value
		previous_value = j
		l += 1
	mean = mean_calc / float(summ)
	mean_list.append(mean)
	l = 1
	rms = 0
	for r in diff[2:]:
		rms += r * (mean - dac_values[l]) ** 2
		l += 1
	rms = math.sqrt(rms / summ)
	rms_list.append(rms)
	diff.append(mean)
	diff.append(rms)
	full_data.append(diff)
	plt.plot(dac_values, data)

rms_mean = numpy.mean(rms_list)
rms_rms = numpy.std(rms_list)

mean_mean = numpy.mean(mean_list)
mean_rms = numpy.std(mean_list)

sub1.set_xlabel('255-CAL_DAC')
sub1.set_ylabel('%')
sub1.set_title('S-curves of all channels')
sub1.grid(True)
text = "%s \n S-curves, 128 channels, HG, 25 ns." % timestamp
sub1.text(25, 140, text, horizontalalignment='center', verticalalignment='center')

sub2 = plt.subplot(413)
sub2.plot(range(0, 128), rms_list,'o')
sub2.set_xlabel('Channel')
sub2.set_ylabel('RMS')
sub2.set_title('RMS of all channels')
sub2.grid(True)
text = "mean: %.2f RMS: %.2f" % (rms_mean, rms_rms)
sub2.text(10, 0.68, text, horizontalalignment='center', verticalalignment='center', bbox=dict(alpha=0.5))

sub3 = plt.subplot(412)
sub3.plot(range(0, 128), mean_list, 'o')
sub3.set_xlabel('Channel')
sub3.set_ylabel('255-CAL_DAC')
sub3.set_title('mean of all channels')
sub3.grid(True)
text = "Mean: %.2f RMS: %.2f" % (mean_mean, mean_rms)
sub3.text(10, 28, text, horizontalalignment='center', verticalalignment='center', bbox=dict(alpha=0.5))

sub4 = plt.subplot(427)
n, bins, patches = sub4.hist(mean_list, bins=30)
sub4.set_ylabel('Occurence')
sub4.set_xlabel('Mean values')
# y = mlab.normpdf(bins, mean_mean, mean_rms)
# sub4.plot(bins, y, 'r--', linewidth=1)

sub5 = plt.subplot(428)
n, bins, patches = sub5.hist(rms_list, bins=30)
sub5.set_ylabel('Occurence')
sub5.set_xlabel('RMS values')
# y = mlab.normpdf(bins, rms_mean, rms_rms)
# sub5.plot(bins, y, 'r--', linewidth=1)

fig.subplots_adjust(hspace=.5)

timestamp = time.strftime("%Y%m%d_%H%M")

fig.savefig("%s%sS-curve_plot.pdf" % (folder, timestamp))

with open("%s%sS-curve_data.csv" % (folder, timestamp), "ab") as f:
	writer = csv.writer(f)
	writer.writerows(full_data)