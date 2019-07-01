#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:00:01 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 13:17:02 2018

@author: mali
"""
import multiprocessing
import time
import pickle
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import comn_conversion as cnvrt
import prnt_plt_anmy as ppanmy

  
  
#==============================================================================
def cnvrt2TDXY_process(rslts_fldr,  rslt_spks_file, w, h):
    t1= time.time()
    print  '### ========================= {} {}x{}============================== '.format(rslt_spks_file, w, h) 
    rslt_spks_fpath = cnvrt.read_flenfldr_ncrntpth( rslts_fldr, rslt_spks_file )
 
    with open(rslt_spks_fpath , 'rb') as spks:
        spks_rslt = pickle.load(spks)
        ld_spks= spks_rslt.segments[0].spiketrains     
    
    
    print '{} :: ld_spks[0].t_stop={}'.format(rslt_spks_file, ld_spks[0].t_stop )
    
    TDXY= cnvrt.frm_spk_trns_to_1D_2D( ld_spks, w, h )
    print TDXY
    print '### {} :: lenght of TDXY : {}, TDXY[0][-1] :  {}'.format( rslt_spks_file, len(TDXY), TDXY[0][-1]  ) 
    
    # store TDXY as pkl file --------------------------------------------------
    pickle_filename = 'TDXY_{}.pickle'.format(rslt_spks_file.split('.')[0])
    tdxy_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@  type: {}, \n name: {}'.format( type(TDXY), tdxy_pth )
    with open( tdxy_pth , 'wb') as handle:
        pickle.dump(TDXY, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print '\n### {} :: store TDXY as pickle file: \n{}'.format(rslt_spks_file,  tdxy_pth)
    print ' {} :: done in {} sec'.format(rslt_spks_file,  time.time()-t1)
    
    with open( tdxy_pth , 'rb') as handle:
        aha = pickle.load(handle)
        print type(aha)
#==============================================================================


if __name__ == "__main__":
    
    rtna_w = 65
    rtna_h = 65
    krnl_sz = 5
    jmp     = 2
    n_rtna  = 2
    rf_orn_vect = [   0 ]
    n_orn  = len ( rf_orn_vect)
    rf_w = (rtna_w - krnl_sz)/jmp +1
    rf_h = (rtna_h - krnl_sz)/jmp +1
    n_lyrs = rf_h

    
    spks_fldr  = 'real_dataset/'
    rslts_fldr = 'rslts/{}'.format(   spks_fldr  )

    rslt_spks_file = 'L_rtna.pickle'
    p0= multiprocessing.Process(target=cnvrt2TDXY_process, 
                                args=(rslts_fldr,  rslt_spks_file, rtna_w, rtna_h)  )  

    rslt_spks_file = 'R_rtna.pickle'
    p10= multiprocessing.Process(target=cnvrt2TDXY_process, 
                                args=(rslts_fldr,  rslt_spks_file, rtna_w, rtna_h)  )
    p0.start()
    p10.start()

    p1=[]
    for orn in range( n_orn ):
        rslt_spks_file = 'L_rf_{}f{}.pickle'.format( rf_orn_vect[orn], n_orn-1)
        p1.append( multiprocessing.Process(target=cnvrt2TDXY_process,  args=(rslts_fldr,rslt_spks_file, rf_w, rf_h)   )     )
        p1[orn].start()
    
    p11=[]
    for orn in range( n_orn ):
        rslt_spks_file = 'R_rf_{}f{}.pickle'.format( rf_orn_vect[orn], n_orn-1)
        p11.append( multiprocessing.Process(target=cnvrt2TDXY_process,  args=(rslts_fldr,rslt_spks_file, rf_w, rf_h)   )     )
        p11[orn].start()
        
        
    p0.join()
    p10.join()
    for orn in range( n_orn ):
        p1[orn].join()
        p11[orn].join()

    print'done!'    
    
#    rslt_spks_file = 'L_rtna.pickle'
#    p0= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rtna_w, rtna_h)  )    
#    rslt_spks_file = 'lft_rf_0f3.pickle'
#    p1= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
##    rslt_spks_file = 'lft_rf_1f3.pickle'
##    p2= multiprocessing.Process(target=cnvrt2TDXY_process, 
##                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
#    rslt_spks_file = 'lft_rf_2f3.pickle'
#    p3= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
##    rslt_spks_file = 'lft_rf_3f3.pickle'
##    p4= multiprocessing.Process(target=cnvrt2TDXY_process, 
##                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )     
#   
#    
#    
#    #--------------------------------------------------------------------------
#    rslt_spks_file = 'rght_rtna.pickle'
#    p10= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rtna_w, rtna_h)  )
#    rslt_spks_file = 'rght_rf_0f3.pickle'
#    p11= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
##    rslt_spks_file = 'rght_rf_1f3.pickle'
##    p12= multiprocessing.Process(target=cnvrt2TDXY_process, 
##                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
#    rslt_spks_file = 'rght_rf_2f3.pickle'
#    p13= multiprocessing.Process(target=cnvrt2TDXY_process, 
#                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
##    rslt_spks_file = 'rght_rf_3f3.pickle'
##    p14= multiprocessing.Process(target=cnvrt2TDXY_process, 
##                                args=(rslts_fldr,  rslt_spks_file, rf_w, rf_h)  )  
##    
#    p0.start()
#    p1.start()
##    p2.start()
#    p3.start()
##    p4.start()
#    
#    p10.start()
#    p11.start()
##    p12.start()
#    p13.start()
##    p14.start()
#
#    
#    p0.join()
#    p1.join()
##    p2.join()
#    p3.join()
##    p4.join()
#    
#    p10.join()
#    p11.join()
##    p12.join()
#    p13.join()
##    p14.join()
 
        








