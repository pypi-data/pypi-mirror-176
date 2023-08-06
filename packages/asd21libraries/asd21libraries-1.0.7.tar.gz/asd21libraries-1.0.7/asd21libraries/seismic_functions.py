import math as M
import numpy as np
from matplotlib import pyplot as plt
import xarray as xr
import binascii
import struct
from scipy import signal


def nearest_pow_2(x):
    '''
    Nearest power of 2
    '''
    
    a = M.pow(2, M.ceil(np.log2(x)))
    b = M.pow(2, M.floor(np.log2(x)))
    if abs(a - x) < abs(b - x):
        return a
    else:
        return b



def Seismic_Waterfall(data,t,offset,xlim=[0,15],ylim=[0,1200],AmpMult=10,recInt=10,winX=15,winY=10,color='k'):
    '''
    Waterfall plot from seismic data
    '''
    
    data = np.transpose(data)
    datatmp = 0*data
    AmpFac = AmpMult/(np.max(np.abs(data[:,1])))
    rec_plot = range(0,np.size(data,1),recInt)
    for ii in range(np.size(data,1)):
        datatmp[:,ii] = AmpFac*data[:,ii] + offset[ii]
    plt.plot(t,datatmp[:,rec_plot],color)
    plt.xlabel('Time (s)')
    plt.ylabel('Rec Number')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.gca().invert_yaxis()
    plt.gcf().set_size_inches(winX,winY)
    plt.show()



def Seismic_SEL(data,rng,Fs,sens=1e5/19.7,plotFlag=True,logFlag=True):
    '''
    Calculate Sound Exposure Level from full array data
    '''
    
    if type(data) == np.ndarray:
        nrec = data.shape[0]
        npts = data.shape[1]
    elif type(data) == xr.core.dataarray.DataArray:
        nrec = len(data.isel(time=0))
        npts = len(data.isel(rec=0))
        
    energy = np.zeros(nrec)
    rec_ind = np.linspace(1,nrec,nrec)

    if type(data) == np.ndarray:
        for i in range(nrec):
            energy[i] = 10*np.log10( np.sum( ( np.abs( data[i,:]*sens ) )**2 )/1e-12 )
            
    elif type(data) == xr.core.dataarray.DataArray:
        for i in range(nrec):
            energy[i] = 10*np.log10( np.sum( ( np.abs( data.isel(rec=i)*sens ) )**2 )/1e-12 )

    SEL = energy
    SELmean = np.mean(SEL)
    SELstd = np.std(SEL)
    yLims = [np.floor((SELmean-2*SELstd)/10)*10,np.ceil((SELmean+2*SELstd)/10)*10]

    if plotFlag == True:
        if logFlag == True:
            fig = plt.figure()
            ax = plt.gca()
            ax.scatter(rng,SEL)
            ax.set_xscale('log')
            plt.grid()
            plt.xlabel('Range (m)')
            plt.ylabel('SEL (dB)')
            plt.ylim(yLims)
        else:
            fig = plt.figure()
            ax = plt.gca()
            ax.scatter(rng,SEL)
            plt.grid()
            plt.xlabel('Range (m)')
            plt.ylabel('SEL (dB)')
            plt.ylim(yLims)
            plt.show()
            
    return SEL




def readP190_2104(filename):
    '''
    Read P190 Navigation file for MGL2104
    '''
    import re

    filename = '/media/asd21/My Passport/MGL2104_PD12_CSs/MGL2104PD12.0.p190'

    RECEIVER_NUMBER = 1200

    class nav:
        numCables = 0
        shotStart = 0
        shotEnd = 0
        depth = []
        vesselX = []
        vesselY = []
        sourceX = []
        sourceY = []
        tailX = []
        tailY = []       
        receiverX = []
        receiverY = []
        receiverZ = []

    file = open(filename, 'r')
    lines = file.readlines()
    receiverX = []
    receiverY = []
    receiverZ = []
    for line in lines:
        if line.startswith('H0101GENERAL'):
            nav.numCables = int(re.sub(r'.*(\d)\sCABLE.*', r'\1 ', line))

        elif line.startswith('H2600Line'):
            nav.shotStart, nav.shotEnd = [int(i) for i in line.split() if i.isdigit()]

        elif line.startswith('VGL') or line.startswith('VMGL'):
            res = line.split('W')
            xyd = (re.sub(r'\.(\d)', r'.\1 ', res[1])).split()
            nav.vesselX.append(float(xyd[0]))
            nav.vesselY.append(float(xyd[1]))
            if len(xyd) >= 3:
                nav.depth.append(float(xyd[2]))
            else:
                nav.depth.append(0)

        elif line.startswith('SGL') or line.startswith('SMGL'):
            res = line.split('W')
            xyd = (re.sub(r'\.(\d)', r'.\1 ', res[1])).split()
            nav.sourceX.append(float(xyd[0]))
            nav.sourceY.append(float(xyd[1]))

        elif line.startswith('CGL') or line.startswith('CMGL'):
            res = line.split('W')
            xyd = (re.sub(r'\.(\d)', r'.\1 ', res[1])).split()
            nav.tailX.append(float(xyd[0]))
            nav.tailY.append(float(xyd[1]))

        elif line.startswith('R'):
          # Add the current receiver arrays to nav and clear them 
            if len(receiverX) == RECEIVER_NUMBER * 1: #nav.numCables:
                nav.receiverX.append(receiverX)
                nav.receiverY.append(receiverY)
                nav.receiverZ.append(receiverZ)
                receiverX = []
                receiverY = []
                receiverZ = []

            length = 26
            receivers = [line[i: i + length] for i in range(1, length * 3 + 1, length)]
            for rec in receivers:
                xyz = (re.sub(r'\.(\d)', r'.\1 ', rec[4:])).split()
                receiverX.append(float(xyz[0]))
                receiverY.append(float(xyz[1]))
                if len(xyz) == 3:
                    receiverZ.append(float(xyz[2]))
                else:
                    receiverZ.append(0)

    return nav



def readSegd2104(filename):
    '''
    
    '''
    # Initializing variables
    class header:
        file_number = 0
        format_code = 0
        gen_consts = 0
        year = 0
        additional_header_blocks = 1
        julian_day = 0
        hour = 0
        minute = 0
        second = 0
        manufacturer_code = 0
        manufacturer_serial_number = 0
        bytes_per_scan = 0
        base_scan_interval = 0
        polarity_code = 0
        scans_in_block_exponent = 0
        scans_in_block_base = 0 
        record_type_code = 0
        record_length = 0
        scans_type_per_record = 0
        channel_set_per_scan_type = 0
        added_skew_fields = 0
        extended_header_length = 0
        external_header_length = 0
        SEGD_revision = 0
        general_trailers = 0
        channel_Set1_channels = 0
        channel_Set2_channels = 0

    # This version only supports reading files with format code 8058. Also this version only reads General Header #1 and General Header #2
    # It does not read any information from any other general headers. It skips reading skew headers, external header blocks, and extended
    # header

    # Mention the location of the file
    with open(filename, 'rb') as f:
        content = f.read()
        temp = binascii.hexlify(content)

        ####### Part 1 - Reading Header Data 

        # Initialising and Computing Variables
        header.file_number = (temp[0:4]).decode('utf-8')
        header.format_code = int(temp[4:8])
        if header.format_code != 8058:
            raise Exception('This File can only read SegD files having format Code 8058')
        header.gen_consts = temp[8:20]
        header.year = int('20' + temp[20:22].decode('utf-8'))
        header.additional_header_blocks = int(temp[22:23])
        header.julian_day = int(temp[23:26])
        header.hour = int(temp[26:28])
        header.minute = int(temp[28:30])
        header.second = int(temp[30:32])
        header.manufacturer_code = int(temp[32:34])
        header.manufacturer_serial_number = int(temp[34:38])
        header.bytes_per_scan = int(temp[38:44])
        header.base_scan_interval = int(temp[44:46])
        header.polarity_code = bin(int(temp[46:47].decode('utf-8')))
        header.record_type_code = bin(int(temp[50:51].decode('utf-8')))
        header.record_length = temp[51:54].decode('utf-8')
        header.scans_type_per_record = int(temp[54:56])
        header.channel_set_per_scan_type = temp[56:58].decode('utf-8')
        header.added_skew_fields = int(temp[58:60])
        header.extended_header_length = temp[60:62].decode('utf-8')
        header.external_header_length = temp[62:64].decode('utf-8') 

        if header.scans_type_per_record > 1:
            raise Exception('This version of readSegD only handles Seg-D files with a single scan type per record')

        # Reading General Header Block #2 
        if header.external_header_length == 'ff':
            header.external_header_length = int(temp[78:82].decode('utf-8'), 16)

        # if header.record_length == 'fff':
        #     header.record_length = int(temp[92:98])

        header.SEGD_revision = float(temp[84:88]) 
        header.general_trailers = temp[88:92].decode('utf-8')


        # This version does not read additional header blocks

        # Reading Scan Type Header
        count = 128 + (header.additional_header_blocks) * 32

        header.channel_Set1_channels = int(temp[count+16:count+20].decode('utf-8'))

        count = count + 64 * int(header.channel_set_per_scan_type)


        # Read Skew Fields
        if header.added_skew_fields > 0:
            count = count + header.added_skew_fields * 32 * 2
            print('Skipping Skew Fields')

        # Read Extended Header
        count = count + int(header.extended_header_length) * 32 * 2
        # print('Skipping Extended Header Blocks')


        # Read External Length
        count = count + int(header.external_header_length) * 32 *2
        # print('Skipping External Header Blocks')

        ###### Part 2 - Reading Trace Data 
        # count = count + 18
        # search = int(temp[count:count + 2].decode('utf-8'))
        
        count = count + 54
        samples_per_trace = (int(temp[count: count + 6], 16))
        # print(samples_per_trace)
        count = count + 434
        # print(count)
        
        add1 = 64
        add2 = 0*8*6001
#         print(temp[count + add1*0 + add2*0:count + add1*1 + add2*0])
#         print(temp[count + add1*1 + add2*1:count + add1*2 + add2*1])
#         print(temp[count + add1*2 + add2*2:count + add1*3 + add2*2])
#         print(temp[count + add1*3 + add2*3:count + add1*4 + add2*3])
        
        data1 = np.zeros((samples_per_trace, header.channel_Set1_channels))
        for j in range(0, header.channel_Set1_channels):
            for i in range(0, samples_per_trace):
                temp1 = temp[count:count + 8].decode('utf-8')
                data1[i][j] = struct.unpack('!f', bytes.fromhex(temp1))[0]
                count = count + 8
                # if j == 1:
                    # print(temp1)
                    # print(data1[i][j])
            count = count + 1*40 + 7*64

        return header, data1
            




def CMPsort(path,files,ShotRec,ShotVol):
    '''
    Sorts through shot volume records to remove common midpoint gathers with inconsistent shot volumes.
    Returns list of "good" CMPs
    '''
    filelist = []
    for file in files:
        ds = xr.open_dataset(path+file)
        FieldRecord = ds['data'].attrs['FieldRecord']
        FieldRecord = [int(x) for x in FieldRecord]
        tmp = np.unique(FieldRecord)
        Vol = []
        for rec in tmp:
            ind = ShotRec.index(rec)
            Vol.append(ShotVol[ind])
        
        if len(np.unique(Vol)) == 1 and Vol[0] > 0.0:
            filelist.append(file)
            
    return filelist



def bathymetry():
    '''
    Plot bathymetry and location of source. 
    Also output vector of bathymetry for each receiver.
    Also output vector of bathymetry for each receiver midpoint.
    '''



def time_stacking(nav,data,DATA,SSP,d_layer):
    
    ci = complex(0,1)
    # print(header.file_number)
    Fs = 500
    nfft = int(data.shape[1]) #int(nearest_pow_2(data.shape[0]))
    f = np.linspace(0,Fs,nfft)

    receiver_no = data.shape[1]
    hydX = nav.receiverX[filenum][0:receiver_no]
    hydY = nav.receiverY[filenum][0:receiver_no]
    hydZ = nav.receiverZ[filenum][0:receiver_no]
    airgunX = nav.sourceX[filenum]
    airgunY = nav.sourceY[filenum]
    x_r = [x - airgunX for x in hydX]
    y_r = [x - airgunY for x in hydY]
    z_r = hydZ

    x_r = np.array(x_r)
    y_r = np.array(y_r)
    z_r = np.array(z_r)
    offset = np.sqrt(x_r**2 + y_r**2)
    
    # START SIMPLE AND ASSUME CONSTANT SSP
    # For loop over each receiver
    dataShift = np.zeros(data.shape)
    t_prop = np.zeros(np.size(data,0))
    
    thetas = np.pi*np.arange(89.9,0,-0.1)/180
    depth = np.arange(0,2981*3,3)
    d_layer_i = np.argmin(np.abs(depth - d_layer))
    
    d_tmp = depth[1:d_layer_i] - depth[0:d_layer_i-1]
    SSP_tmp = SSP[1:d_layer_i]
    ii = 0
    X_all = np.zeros(len(thetas))
    # print(thetas)
    for th_tmp in thetas:
        # X_all[ii] = 2*np.sum( d_tmp * 1480 * np.cos( np.arcsin( SSP_tmp/1480*np.sin(th_tmp) ) ) / (SSP_tmp * np.sin(th_tmp) ) )
        X_all[ii] = 2*np.sum( d_tmp / (np.tan(np.arccos(SSP_tmp/1480*np.cos(th_tmp)))) )
        if np.isnan(X_all[ii]) == True:
            X_all[ii] = X_all[ii-1]
        ii += 1
    
    th_save = np.zeros(len(offset))
    ii = 0
    
    for Rtmp in offset:
        r_i = np.argmin(np.abs(X_all - Rtmp))
        th_save[ii] = thetas[r_i]
        ii += 1
        
    for rec in range(np.size(data,0)):
        
        Rtmp = offset[rec]
        th_tmp = th_save[rec]
        t_prop[rec] = 2*np.sum( d_tmp / (SSP_tmp*np.sin(np.arccos(SSP_tmp/1480*np.cos(th_tmp)))) )
        # t_prop[rec] = 2*np.sum( 1480*d_tmp/(SSP_tmp**2 * np.sin(th_tmp)) )
        
#         th = np.arctan(2*d_layer/Rtmp)
        
#         t_prop[rec] = d_layer/np.sin(th)*2/1500
        
        dataShift[rec,:] = np.fft.ifft( DATA[rec,:]*np.exp(ci*2*np.pi*f*(t_prop[rec]-1)) )
        
    dataSum = np.sum(dataShift,0)
    dataAbsSum = np.sum(np.abs(dataShift),0)
    
    return dataAbsSum, dataSum
    
    



def ref_coeff(data,offset,depth,Fs,spreadFlag = False, beamdata = False, c = 1485.0, tleft = 0.25, tright = 1.75):
    '''
    Generate reflection coefficient data
    '''
        
    samples = np.size(data,1)
    nrec = np.size(data,0)
    angles = np.arctan(2*depth/offset)
    freq_energy = np.zeros([nrec,samples])
    freq_direnergy = np.zeros([nrec,samples])
    freq_refenergy = np.zeros([nrec,samples])
    freq_ref2energy = np.zeros([nrec,samples])
    refCoeff1 = np.zeros([nrec,int(samples/2)])
    refCoeff2 = np.zeros([nrec,int(samples/2)])
    refCoeff3 = np.zeros([nrec,int(samples/2)])

    if beamdata == False:
        beamdata = np.ones([91,250])

    for i in range(nrec):
        angle = angles[i]
        angle_i = int(np.round(angle))
        angle_i2 = int((np.round(angle)+90)/2)
        
        # Calculate energy at each receiver/frequency
        freq_energy = np.abs(np.fft.fft(data[i,:],samples))[0:int(samples/2)]

        # Calculate energy direct path
        t_delay = offset[i]/c
        tspan = [t_delay-0.2,t_delay+0.2]
        ti = [int(tspan[0]*Fs),int(tspan[1]*Fs)]
        tsamp = ti[1]-ti[0]
        datatmp = np.append(data[i,ti[0]:ti[1]],np.zeros(samples-tsamp))
        beamtmp = np.interp(np.linspace(0,Fs/2,int(samples/2)), np.arange(0,Fs/2,1), beamdata[0,:])
        freq_direnergy = np.abs(np.fft.fft(datatmp,tsamp))

        # Calculate energy first reflection
        t_delay = np.sqrt(offset[i]**2 + (2*depth)**2)/c
        tspan = [t_delay-tleft,t_delay+tright]
        ti = [int(tspan[0]*Fs),int(tspan[1]*Fs)]
        tsamp = ti[1]-ti[0]
        datatmp = np.append(data[i,ti[0]:ti[1]],np.zeros(samples-tsamp))
        beamtmp = np.interp(np.linspace(0,Fs/2,int(samples/2)), np.arange(0,Fs/2,1), beamdata[angle_i,:])
        freq_refenergy = np.abs(np.fft.fft(datatmp,tsamp))

        # Calculate energy second reflection
        t_delay = np.sqrt(offset[i]**2 + (4*depth)**2)/c
        tspan = [t_delay-tleft,t_delay+tright]
        ti = [int(tspan[0]*Fs),int(tspan[1]*Fs)]
        tsamp = ti[1]-ti[0]
        datatmp = np.append(data[i,ti[0]:ti[1]],np.zeros(samples-tsamp))
        beamtmp = np.interp(np.linspace(0,Fs,tsamp), np.arange(0,Fs/2,1), beamdata[angle_i2,:])
        freq_ref2energy = np.abs(np.fft.fft(datatmp,tsamp))

        if spreadFlag == True:
            freq_direnergy = freq_direnergy*offset[i]
            freq_refenergy = freq_refenergy_tmp*np.sqrt(offset[i]**2 + (2*depth)**2)
            freq_ref2energy = freq_ref2energy_tmp*np.sqrt(offset[i]**2 + (4*depth)**2)


        i = 0
        freqs = np.linspace(0,Fs,samples)

        # Calculate reflection coefficients
        refDirTmp = freq_refenergy/freq_direnergy
        ref2DirTmp = freq_ref2energy/freq_direnergy
        ref2refTmp = freq_ref2energy/freq_refenergy

        # Remove negative frequencies
        refCoeff1[i,:] = refDirTmp[0:int(samples/2)]
        refCoeff2[i,:] = refDirTmp[0:int(samples/2)]
        refCoeff3[i,:] = refDirTmp[0:int(samples/2)]

    # Normalize reflection coefficient
    refCoeffNorm1 = refCoeff1/np.max(refCoeff1)
    refCoeffNorm2 = refCoeff2/np.max(refCoeff2)
    refCoeffNorm3 = refCoeff3/np.max(refCoeff3)

    return angles, refCoeffNorm1, refCoeffNorm2, refCoeffNorm3
