import wave, struct
from array import *

def wavRead(fname, spkr_info, labfile, dst_folder):
    txt_list = ['14_01_001_rp_0','14_03_001','14_03_002','14_04_001','14_04_002','14_05_001','14_05_002','14_05_003','14_05_004','14_05_005','14_06_001','14_06_002','14_06_003','14_01_001_rp_1','20_18_001','20_18_002','20_18_003','20_18_004','20_18_005','20_18_006','20_20_001','20_20_002','20_20_003','20_20_004','20_20_005','20_20_006','20_07_001','20_07_002','20_07_003','20_07_004','20_07_005','20_07_006','20_07_007','20_07_008','20_01_001','20_01_002','20_01_003','20_01_004','20_19_001','20_19_002','20_19_003','20_19_004','20_03_001','20_03_002','20_04_001','20_04_002','20_05_001','14_01_001_rp_2']
    fid =  open(labfile,'r')
    all_lines = fid.readlines()
    fid.close()

    print str(len(all_lines))+' segments in lab file'
    waveFile = wave.open(fname, 'rb')
    
        
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = waveFile.getparams()
    print ("======", nchannels, sampwidth, framerate, nframes, comptype, compname)
    frames = waveFile.readframes (nframes * nchannels)
    out = struct.unpack_from("%dh" % nframes * nchannels, frames)

    # Convert 2 channles to numpy arrays
    if nchannels == 2:
        left  = array (list (out[0::2]))
        right = array (list (out[1::2]))
    else:
        left = array('i', out)
        right = left
        
    print(str(len(left))+ ' samples in wav audio')

    for i in range(len(all_lines)):
        ln = all_lines[i]
        txt = txt_list[i]
        temp = ln.strip().split(' ')
        print temp
        st = int(float(temp[0])*framerate)
        ed = int(float(temp[1])*framerate)

        #outFileName = fname.strip('.')[0]+'_'str(i+1)+'_'+txt+'.wav'
        outFileName = dst_folder+'/'+spkr_info+'_'+txt+'_'+str(i+1)+'.wav'
        print fname.strip('.wav')
        print outFileName
        ofile = wave.open(outFileName, 'w')
            #nchannels, sampwidth, framerate, nframes, comptype, compname
            #save only one channel
        ofile.setparams((1, sampwidth, framerate, 0, 'NONE', 'not compressed'))
        wvData=""
        for j in range(st, ed): 
            wvData += struct.pack('h', left[j]) 
        ofile.writeframes(wvData)
        ofile.close()

            
    waveFile.close()
    
filename = r'D:/testing_corpus/recording/025_tanrunze_guangdong.wav' #'wy_nihao_20151022.wav' #xiaoyi.wav'
spkr_info = r'025M22_01'
labfile = r'D:/testing_corpus/'+spkr_info+'.csv'
dst_folder = r'D:/testing/'
wavRead(filename, spkr_info, labfile, dst_folder)
