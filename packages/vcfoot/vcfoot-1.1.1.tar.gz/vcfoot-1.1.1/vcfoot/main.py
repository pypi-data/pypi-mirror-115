import math #line:2
from scipy import signal #line:3
from copy import deepcopy #line:4
import numpy as np #line:5
import cv2 #line:6
import pickle #line:7
from vcopt import vcopt #line:8
try :#line:10
    from foot_tool import ft ,pl_class ,cl_class #line:11
    print ('import normal version')#line:12
except :#line:13
    from .foot_tool import ft ,pl_class ,cl_class #line:14
    print ('import . version')#line:15
class vcfoot :#line:20
    def __init__ (OO0OOOO0OOO0OO0O0 ):#line:21
        pass #line:22
    def __del__ (O00OOOOO0O00OO0O0 ):#line:23
        pass #line:24
    def level (OOOO00O0O0OO00O00 ,OO0000OO0OO0O00OO ,url =None ,flip =False ,save =None ,test =0 ):#line:27
        print ('\n### objファイルの読み込み')#line:29
        O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,O0OO0OOOO00OO00OO =ft .load_obj (OO0000OO0OO0O00OO )#line:31
        if np .max (O0000O0O0O00OOOOO )<=1.0 :#line:33
            O0000O0O0O00OOOOO =np .array (O0000O0O0O00OOOOO *255.0 ,int )#line:34
        O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 =ft .down_sample (O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,20000 )#line:36
        if test :#line:37
            ft .showc (O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 ,'xz')#line:38
        print ('\n### 静置GA')#line:44
        try :#line:46
            OOOOO0O0O000OO0OO #line:47
        except NameError :#line:48
            print ('\n### ダウンサンプル')#line:50
            O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 =ft .down_sample (O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,8000 )#line:52
            def O0O000OOO000O000O (O000O0OOO0O00OOOO ):#line:55
                OOOO0OO00000OO0OO =deepcopy (O0O00OOOO0OO00OO0 )#line:57
                OOOO0OO00000OO0OO =ft .rotate_3D_x (OOOO0OO00000OO0OO ,O000O0OOO0O00OOOO [0 ])#line:58
                OOOO0OO00000OO0OO =ft .rotate_3D_y (OOOO0OO00000OO0OO ,O000O0OOO0O00OOOO [1 ])#line:59
                OOO0OOOO0OO0O000O ,OOOO00O00O00OO0O0 =np .histogram (OOOO0OO00000OO0OO [:,2 ],bins =50 )#line:61
                O0000OO0O0O0OO0OO =4 #line:63
                OOOO0O000O000000O =np .ones (O0000OO0O0O0OO0OO )/O0000OO0O0O0OO0OO #line:64
                O0O00OO0OO0OOOO00 =signal .convolve (OOO0OOOO0OO0O000O ,OOOO0O000O000000O ,mode ='same')#line:65
                OOOO00O0OO0OOOO0O =np .max (O0O00OO0OO0OOOO00 )#line:67
                return OOOO00O0OO0OOOO0O #line:68
            def O000O00OOOOO0OO0O ():#line:71
                O00OO000O00O00OO0 =[[0 ,180 ],[0 ,180 ]]#line:73
                O00O0O0O00O00O00O ,OOOOO0OO000OOO000 =vcopt ().rcGA (O00OO000O00O00OO0 ,O0O000OOO000O000O ,99999 ,show_pool_func ='bar',seed ='grendel_master_eternity',pool_num =100 ,core_num =8 ,max_gen =10000 )#line:82
                return O00O0O0O00O00O00O #line:83
            print ('\n### 静置GA')#line:86
            OOOOO0O0O000OO0OO =O000O00OOOOO0OO0O ()#line:88
            print ('para = [{}, {}]'.format (OOOOO0O0O000OO0OO [0 ],OOOOO0O0O000OO0OO [1 ]))#line:90
        print ('\n### 反映')#line:94
        O0O000O00OO0OO00O =ft .rotate_3D_x (O0O000O00OO0OO00O ,OOOOO0O0O000OO0OO [0 ])#line:96
        O0O000O00OO0OO00O =ft .rotate_3D_y (O0O000O00OO0OO00O ,OOOOO0O0O000OO0OO [1 ])#line:97
        print ('\n### 確認')#line:102
        O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 =ft .down_sample (O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,20000 )#line:104
        if test :#line:105
            ft .showc (O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 ,'xz')#line:106
        print ('\n### 逆さなら反転')#line:118
        OOO0O00O0OOOO0OOO =np .median (O0O000O00OO0OO00O [:,2 ])#line:121
        OO0OOOOO000OO0O0O =np .mean (O0O000O00OO0OO00O [:,2 ])#line:122
        OOOO000O0000O0O0O =OO0OOOOO000OO0O0O >OOO0O00O0OOOO0OOO #line:123
        print ('up_bool:\n{}'.format (OOOO000O0000O0O0O ))#line:124
        if OOOO000O0000O0O0O ==True :#line:126
            if flip ==False :#line:128
                pass #line:129
            if flip ==True :#line:131
                print ('強制反転')#line:132
                O0O000O00OO0OO00O =ft .rotate_3D_x (O0O000O00OO0OO00O ,180 )#line:133
        else :#line:135
            if flip ==False :#line:137
                print ('通常反転')#line:138
                O0O000O00OO0OO00O =ft .rotate_3D_x (O0O000O00OO0OO00O ,180 )#line:139
            if flip ==True :#line:142
                pass #line:143
        print ('\n### 確認')#line:146
        O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 =ft .down_sample (O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,20000 )#line:148
        if test :#line:149
            ft .showc (O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 ,'xz')#line:150
        print ('\n### zレベル補正')#line:155
        OO0OOOO000O0OO0O0 ,OO00OO000O0OO00O0 =np .histogram (O0O000O00OO0OO00O [:,2 ],bins =100 )#line:158
        OO0O00O0OO0OO0O00 =4 #line:160
        OOOOOO0O000O0OOOO =np .ones (OO0O00O0OO0OO0O00 )/OO0O00O0OO0OO0O00 #line:161
        O0OOO0O00O0OO0OOO =signal .convolve (OO0OOOO000O0OO0O0 ,OOOOOO0O000O0OOOO ,mode ='same')#line:162
        O0O0000O00OOO0O0O =OO00OO000O0OO00O0 [np .argmax (O0OOO0O00O0OO0OOO )]#line:164
        print ('z_level:\n{}'.format (O0O0000O00OOO0O0O ))#line:165
        O0O000O00OO0OO00O [:,2 ]-=O0O0000O00OOO0O0O #line:167
        O0O000O00OO0OO00O [:,0 ]-=np .min (O0O000O00OO0OO00O [:,0 ])#line:170
        O0O000O00OO0OO00O [:,1 ]-=np .min (O0O000O00OO0OO00O [:,1 ])#line:171
        print ('\n### 確認')#line:174
        O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 =ft .down_sample (O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,20000 )#line:176
        if test :#line:177
            ft .showc (O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 ,'xz')#line:178
        if save !=None :#line:180
            print ('\n### 保存')#line:182
            with open (save ,'wb')as O0000000O00OO00OO :#line:184
                pickle .dump ([O0O000O00OO0OO00O ,O0000O0O0O00OOOOO ,O0OO0OOOO00OO00OO ],O0000000O00OO00OO )#line:185
            ft .showc (O0O00OOOO0OO00OO0 ,OOO00OOO00OO00O00 ,'xz',save =save +'.png')#line:186
    def enkaku (OOOO0O0O00000OO00 ,O0OO0OO00O0O00O00 ,paper_long =297 ,paper_short =210 ,window_size =900 ,dot_size =1 ,cut_height =120 ,rate1 =0.18 ,rate2 =0.44 ,rate3 =0.54 ,test =0 ):#line:209
        print ('\n### pcklファイルの読み込み')#line:247
        if O0OO0OO00O0O00O00 [:4 ]=='http':#line:250
            OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,O0OO0OO0OOOO0000O =ft .load_pckl_url (O0OO0OO00O0O00O00 )#line:251
        else :#line:252
            OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,O0OO0OO0OOOO0000O =ft .load_pckl (O0OO0OO00O0O00O00 )#line:253
        if np .max (OO0OOOOOO00O00000 )<=1.0 :#line:255
            OO0OOOOOO00O00000 =np .array (OO0OOOOOO00O00000 *255.0 ,int )#line:256
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:258
        if test :#line:259
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xz')#line:260
        print ('\n### 紙の大きさにカット')#line:268
        try :#line:270
            O0000O00OOOOOOO00 #line:271
            O00OOO000O0O0OOO0 #line:272
        except NameError :#line:273
            print ('\n### ダウンサンプル')#line:275
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,200000 )#line:277
            print ('\n### 前処理')#line:280
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:283
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 )#line:285
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Center of paper','2, Select cut range (about)'])#line:288
            O00O000OO0OO0O0O0 ='step1'#line:297
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:298
            OOOO00OOOOO00OO0O =2 #line:299
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:300
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:301
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:302
            cv2 .waitKey ()#line:303
            print ('\n### 後処理')#line:306
            O0000O00OOOOOOO00 =np .array (O00000OOOO0O0OOO0 .p [0 ],float )#line:309
            O00OOO000O0O0OOO0 =max (abs (O00000OOOO0O0OOO0 .p [1 ,0 ]-O00000OOOO0O0OOO0 .p [0 ,0 ]),abs (O00000OOOO0O0OOO0 .p [1 ,1 ]-O00000OOOO0O0OOO0 .p [0 ,1 ]))#line:310
            O0000O00OOOOOOO00 =O0000O00OOOOOOO00 /O00O0O0OO0OO000OO #line:313
            O00OOO000O0O0OOO0 =O00OOO000O0O0OOO0 /O00O0O0OO0OO000OO #line:314
            print ('cut_center = [{}, {}]'.format (O0000O00OOOOOOO00 [0 ],O0000O00OOOOOOO00 [1 ]))#line:315
            print ('cut_len = {}'.format (O00OOO000O0O0OOO0 ))#line:316
        print ('\n### 反映')#line:320
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,0 ]>O0000O00OOOOOOO00 [1 ]-O00OOO000O0O0OOO0 ]#line:323
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,0 ]>O0000O00OOOOOOO00 [1 ]-O00OOO000O0O0OOO0 ]#line:324
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,0 ]<O0000O00OOOOOOO00 [1 ]+O00OOO000O0O0OOO0 ]#line:325
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,0 ]<O0000O00OOOOOOO00 [1 ]+O00OOO000O0O0OOO0 ]#line:326
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,1 ]>O0000O00OOOOOOO00 [0 ]-O00OOO000O0O0OOO0 ]#line:328
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,1 ]>O0000O00OOOOOOO00 [0 ]-O00OOO000O0O0OOO0 ]#line:329
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,1 ]<O0000O00OOOOOOO00 [0 ]+O00OOO000O0O0OOO0 ]#line:330
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,1 ]<O0000O00OOOOOOO00 [0 ]+O00OOO000O0O0OOO0 ]#line:331
        OOOO0OO00000O0000 [:,0 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:336
        OOOO0OO00000O0000 [:,1 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:337
        print ('\n### 確認')#line:340
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:342
        if test :#line:344
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xy')#line:345
        print ('\n### 紙のサイズ校正')#line:357
        try :#line:359
            OOO00O000OO000O00 #line:360
            O000OO00OOO0O0000 #line:361
            O00000OO00O00OOO0 #line:362
        except NameError :#line:363
            print ('\n### ダウンサンプル')#line:365
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,200000 )#line:367
            print ('\n### 前処理')#line:370
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:373
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 )#line:375
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Top-left of paper','2, Bottom-right of paper'])#line:378
            O00O000OO0OO0O0O0 ='step2'#line:384
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:385
            OOOO00OOOOO00OO0O =2 #line:386
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:387
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:388
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:389
            cv2 .waitKey ()#line:390
            print ('\n### 後処理')#line:393
            O000OO00OOO0O0000 =np .array (O00000OOOO0O0OOO0 .p [0 ],float )/O00O0O0OO0OO000OO #line:396
            print ('top_left = [{}, {}]'.format (O000OO00OOO0O0000 [0 ],O000OO00OOO0O0000 [1 ]))#line:397
            O00000OO00O00OOO0 =np .array (O00000OOOO0O0OOO0 .p [1 ],float )/O00O0O0OO0OO000OO #line:400
            print ('bottom_right = [{}, {}]'.format (O00000OO00O00OOO0 [0 ],O00000OO00O00OOO0 [1 ]))#line:401
            O0O0000OOOO0OOOOO =math .atan2 (O00000OO00O00OOO0 [1 ]-O000OO00OOO0O0000 [1 ],O00000OO00O00OOO0 [0 ]-O000OO00OOO0O0000 [0 ])#line:404
            OOOO0O0OOOOO00000 =math .degrees (O0O0000OOOO0OOOOO )#line:406
            OO0O000OOOO0000OO =math .atan2 (paper_long ,paper_short )#line:410
            OO000OO0000OO0O00 =math .degrees (OO0O000OOOO0000OO )#line:412
            OOO00O000OO000O00 =OO000OO0000OO0O00 -OOOO0O0OOOOO00000 #line:416
            if OOO00O000OO000O00 >180 :#line:417
                OOO00O000OO000O00 =-360 +OOO00O000OO000O00 #line:418
            if OOO00O000OO000O00 <-180 :#line:419
                OOO00O000OO000O00 =360 -OOO00O000OO000O00 #line:420
            print ('rotation_paper = {}'.format (OOO00O000OO000O00 ))#line:421
        print ('\n### 反映')#line:425
        O000OO00OOO0O0000 =ft .rotate_2D_z (O000OO00OOO0O0000 ,theta =-OOO00O000OO000O00 )#line:428
        O00000OO00O00OOO0 =ft .rotate_2D_z (O00000OO00O00OOO0 ,theta =-OOO00O000OO000O00 )#line:429
        OOOO0OO00000O0000 =ft .rotate_3D_z (OOOO0OO00000O0000 ,theta =-OOO00O000OO000O00 )#line:430
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,0 ]>O000OO00OOO0O0000 [1 ]]#line:433
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,0 ]>O000OO00OOO0O0000 [1 ]]#line:434
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,0 ]<O00000OO00O00OOO0 [1 ]]#line:435
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,0 ]<O00000OO00O00OOO0 [1 ]]#line:436
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,1 ]>O000OO00OOO0O0000 [0 ]]#line:438
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,1 ]>O000OO00OOO0O0000 [0 ]]#line:439
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,1 ]<O00000OO00O00OOO0 [0 ]]#line:440
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,1 ]<O00000OO00O00OOO0 [0 ]]#line:441
        OO000OO00O0OO0OO0 =O00000OO00O00OOO0 [0 ]-O000OO00OOO0O0000 [0 ]#line:444
        OOOO0O00O00OOOO0O =O00000OO00O00OOO0 [1 ]-O000OO00OOO0O0000 [1 ]#line:445
        OOOOOOO000000OOOO =paper_short /OO000OO00O0OO0OO0 #line:447
        OOO0O0OO0O0O00O0O =paper_long /OOOO0O00O00OOOO0O #line:448
        O00O0O0OO0OO000OO =(OOOOOOO000000OOOO +OOO0O0OO0O0O00O0O )/2 #line:452
        O000OO00OOO0O0000 *=O00O0O0OO0OO000OO #line:455
        O00000OO00O00OOO0 *=O00O0O0OO0OO000OO #line:456
        OOOO0OO00000O0000 *=O00O0O0OO0OO000OO #line:457
        OO0OOOOOO00O00000 =OO0OOOOOO00O00000 [OOOO0OO00000O0000 [:,2 ]<cut_height ]#line:461
        OOOO0OO00000O0000 =OOOO0OO00000O0000 [OOOO0OO00000O0000 [:,2 ]<cut_height ]#line:462
        O000OO00OOO0O0000 [1 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:465
        O000OO00OOO0O0000 [0 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:466
        O00000OO00O00OOO0 [1 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:467
        O00000OO00O00OOO0 [0 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:468
        OOOO0OO00000O0000 [:,0 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:469
        OOOO0OO00000O0000 [:,1 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:470
        print ('\n### 確認')#line:474
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:476
        if test :#line:477
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xy',O000OO00OOO0O0000 ,O00000OO00O00OOO0 )#line:478
        print ('\n### 足の向き補正')#line:496
        try :#line:498
            O0OO000OO0O0O000O #line:499
            O00O0O000O000OOOO #line:500
            O00O00O00O0O000O0 #line:501
        except NameError :#line:502
            print ('\n### ダウンサンプル')#line:504
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,200000 )#line:506
            print ('\n### 前処理')#line:509
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:512
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 )#line:514
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Second-finger tip','2, Heel tip'],right =True )#line:517
            O00O000OO0OO0O0O0 ='step3'#line:523
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:524
            OOOO00OOOOO00OO0O =2 #line:525
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:526
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:527
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:528
            cv2 .waitKey ()#line:529
            print ('\n### 後処理')#line:532
            O0OO000OO0O0O000O =np .array (O00000OOOO0O0OOO0 .p [0 ],float )/O00O0O0OO0OO000OO #line:535
            print ('foot_tip = [{}, {}]'.format (O0OO000OO0O0O000O [0 ],O0OO000OO0O0O000O [1 ]))#line:536
            O00O0O000O000OOOO =np .array (O00000OOOO0O0OOO0 .p [1 ],float )/O00O0O0OO0OO000OO #line:539
            print ('heel_tip = [{}, {}]'.format (O00O0O000O000OOOO [0 ],O00O0O000O000OOOO [1 ]))#line:540
            O0O0000OOOO0OOOOO =math .atan2 (O00O0O000O000OOOO [1 ]-O0OO000OO0O0O000O [1 ],O00O0O000O000OOOO [0 ]-O0OO000OO0O0O000O [0 ])#line:543
            OOOO0O0OOOOO00000 =math .degrees (O0O0000OOOO0OOOOO )#line:544
            O00O00O00O0O000O0 =OOOO0O0OOOOO00000 -90 #line:546
            if O00O00O00O0O000O0 >180 :#line:548
                O00O00O00O0O000O0 =-360 +O00O00O00O0O000O0 #line:549
            if O00O00O00O0O000O0 <-180 :#line:550
                O00O00O00O0O000O0 =360 -O00O00O00O0O000O0 #line:551
            print ('rotation_foot = {}'.format (O00O00O00O0O000O0 ))#line:552
        print ('\n### 反映')#line:555
        O0OO000OO0O0O000O =ft .rotate_2D_z (O0OO000OO0O0O000O ,theta =O00O00O00O0O000O0 )#line:558
        O00O0O000O000OOOO =ft .rotate_2D_z (O00O0O000O000OOOO ,theta =O00O00O00O0O000O0 )#line:559
        OOOO0OO00000O0000 =ft .rotate_3D_z (OOOO0OO00000O0000 ,theta =O00O00O00O0O000O0 )#line:560
        O0OO000OO0O0O000O [1 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:564
        O0OO000OO0O0O000O [0 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:565
        O00O0O000O000OOOO [1 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:566
        O00O0O000O000OOOO [0 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:567
        OOOO0OO00000O0000 [:,0 ]-=np .min (OOOO0OO00000O0000 [:,0 ])#line:568
        OOOO0OO00000O0000 [:,1 ]-=np .min (OOOO0OO00000O0000 [:,1 ])#line:569
        print ('\n### 確認')#line:573
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:575
        if test :#line:576
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xy',O0OO000OO0O0O000O ,O00O0O000O000OOOO )#line:577
        print ('\n### 足の測定１')#line:596
        try :#line:598
            OOO000OO000O0O000 #line:599
            O00OOOO0O00000000 #line:600
            O00OOOOOOO000OOOO #line:601
            OO00OOO0O0OOO0OOO #line:602
            OOOOO000OO000OO0O #line:603
            OO0O0OOO0OO00O0O0 #line:604
            OOOOOOOOOO00OOO00 #line:605
            OOOOOO0OOOOO0O0O0 #line:606
            OO00O00O0O0000OOO #line:607
        except NameError :#line:608
            print ('\n### ダウンサンプル')#line:610
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,200000 )#line:612
            print ('\n### 前処理')#line:615
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:618
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 )#line:620
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Toe tip','2, Heel tip','3, Heel-left','4, Heel-right','5, Width-left','6, Width-right'],right =True )#line:627
            O00O000OO0OO0O0O0 ='step4'#line:633
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:634
            OOOO00OOOOO00OO0O =6 #line:635
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:636
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:637
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:638
            cv2 .waitKey ()#line:639
            print ('\n### 後処理')#line:642
            OO00O0OOO000O0O00 ,OO0OO0000OO0OOO00 =O00000OOOO0O0OOO0 .p [0 ]/O00O0O0OO0OO000OO #line:645
            OOO00OOO0O0O00000 ,O00000OOOO00OO0OO =O00000OOOO0O0OOO0 .p [1 ]/O00O0O0OO0OO000OO #line:646
            O00O0OO0O0OO0OO0O ,O0O000O00OO0000OO =O00000OOOO0O0OOO0 .p [2 ]/O00O0O0OO0OO000OO #line:647
            OO0OO0OO000OO00O0 ,O0OOO0OOOOO0OO0OO =O00000OOOO0O0OOO0 .p [3 ]/O00O0O0OO0OO000OO #line:648
            O0OOOO00OO00OOO00 ,O0OO0O0000OO00OO0 =O00000OOOO0O0OOO0 .p [4 ]/O00O0O0OO0OO000OO #line:649
            OOO0O0O00O00OO000 ,O00OO000O0O00O0O0 =O00000OOOO0O0OOO0 .p [5 ]/O00O0O0OO0OO000OO #line:650
            OOO000OO000O0O000 =abs (O00000OOOO00OO0OO -OO0OO0000OO0OOO00 )#line:653
            print ('l_foot = {}'.format (OOO000OO000O0O000 ))#line:654
            O00OOOO0O00000000 =abs (OO0OO0OO000OO00O0 -O00O0OO0O0OO0OO0O )#line:656
            print ('w_heel = {}'.format (O00OOOO0O00000000 ))#line:657
            O00OOOOOOO000OOOO =((OOO0O0O00O00OO000 -O0OOOO00OO00OOO00 )**2 +(O00OO000O0O00O0O0 -O0OO0O0000OO00OO0 )**2 )**0.5 #line:659
            print ('w_foot = {}'.format (O00OOOOOOO000OOOO ))#line:660
            OO00OOO0O0OOO0OOO =[O0OOOO00OO00OOO00 ,O0OO0O0000OO00OO0 ]#line:662
            OOOOO000OO000OO0O =[OOO0O0O00O00OO000 ,O00OO000O0O00O0O0 ]#line:663
            print ('w_point1 = [{}, {}]'.format (OO00OOO0O0OOO0OOO [0 ],OO00OOO0O0OOO0OOO [1 ]))#line:664
            print ('w_point2 = [{}, {}]'.format (OOOOO000OO000OO0O [0 ],OOOOO000OO000OO0O [1 ]))#line:665
            OO0O0OOO0OO00O0O0 =abs (O00000OOOO00OO0OO -O0OO0O0000OO00OO0 )#line:667
            OOOOOOOOOO00OOO00 =abs (O00000OOOO00OO0OO -O00OO000O0O00O0O0 )#line:668
            print ('w_level_left = {}'.format (OO0O0OOO0OO00O0O0 ))#line:669
            print ('w_level_right = {}'.format (OOOOOOOOOO00OOO00 ))#line:670
            OOOOOO0OOOOO0O0O0 =abs (O00O0O000O000OOOO [0 ]-O0OOOO00OO00OOO00 )#line:672
            OO00O00O0O0000OOO =abs (OOO0O0O00O00OO000 -O00O0O000O000OOOO [0 ])#line:673
            print ('w_len_left = {}'.format (OOOOOO0OOOOO0O0O0 ))#line:674
            print ('w_len_right = {}'.format (OO00O00O0O0000OOO ))#line:675
        print ('\n### 確認')#line:678
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:680
        if test :#line:681
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xy',O0OO000OO0O0O000O ,O00O0O000O000OOOO ,OO00OOO0O0OOO0OOO ,OOOOO000OO000OO0O )#line:682
        print ('\n### 足囲の取り出し')#line:695
        O0OOO0O0O00000OO0 =deepcopy (OOOO0OO00000O0000 )#line:698
        O00O00O0000OOO0O0 =deepcopy (OO0OOOOOO00O00000 )#line:699
        O0O0000OOOO0OOOOO =math .atan2 (OOOOO000OO000OO0O [0 ]-OO00OOO0O0OOO0OOO [0 ],OOOOO000OO000OO0O [1 ]-OO00OOO0O0OOO0OOO [1 ])#line:702
        OOOO0O0OOOOO00000 =math .degrees (O0O0000OOOO0OOOOO )#line:703
        OOO0OOOOOO0OO0O0O =90 -OOOO0O0OOOOO00000 #line:705
        if OOO0OOOOOO0OO0O0O >180 :#line:707
            OOO0OOOOOO0OO0O0O =-360 +OOO0OOOOOO0OO0O0O #line:708
        if OOO0OOOOOO0OO0O0O <-180 :#line:709
            OOO0OOOOOO0OO0O0O =360 -OOO0OOOOOO0OO0O0O #line:710
        OO00OOO0O0OOO0OOO =ft .rotate_2D_z (OO00OOO0O0OOO0OOO ,theta =OOO0OOOOOO0OO0O0O )#line:714
        OOOOO000OO000OO0O =ft .rotate_2D_z (OOOOO000OO000OO0O ,theta =OOO0OOOOOO0OO0O0O )#line:715
        O0OOO0O0O00000OO0 =ft .rotate_3D_z (O0OOO0O0O00000OO0 ,theta =OOO0OOOOOO0OO0O0O )#line:716
        O0O00OO0O000OO00O =(O0OOO0O0O00000OO0 [:,0 ]>OO00OOO0O0OOO0OOO [1 ]-2 )*(O0OOO0O0O00000OO0 [:,0 ]<OO00OOO0O0OOO0OOO [1 ]+2 )#line:719
        O0OOO0O0O00000OO0 =O0OOO0O0O00000OO0 [O0O00OO0O000OO00O ]#line:720
        O00O00O0000OOO0O0 =O00O00O0000OOO0O0 [O0O00OO0O000OO00O ]#line:721
        OO00OOO0O0OOO0OOO [1 ]-=np .min (O0OOO0O0O00000OO0 [:,0 ])#line:724
        OO00OOO0O0OOO0OOO [0 ]-=np .min (O0OOO0O0O00000OO0 [:,1 ])#line:725
        OOOOO000OO000OO0O [1 ]-=np .min (O0OOO0O0O00000OO0 [:,0 ])#line:726
        OOOOO000OO000OO0O [0 ]-=np .min (O0OOO0O0O00000OO0 [:,1 ])#line:727
        O0OOO0O0O00000OO0 [:,0 ]-=np .min (O0OOO0O0O00000OO0 [:,0 ])#line:728
        O0OOO0O0O00000OO0 [:,1 ]-=np .min (O0OOO0O0O00000OO0 [:,1 ])#line:729
        if test :#line:731
            ft .showc (O0OOO0O0O00000OO0 ,O00O00O0000OOO0O0 ,'xy',OO00OOO0O0OOO0OOO ,OOOOO000OO000OO0O )#line:732
        print ('\n### 足囲')#line:736
        try :#line:738
            OOOO0O0OOOOOOO0O0 #line:739
        except NameError :#line:740
            print ('\n### ダウンサンプル')#line:742
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (O0OOO0O0O00000OO0 ,O00O00O0000OOO0O0 ,200000 )#line:744
            print ('\n### 前処理')#line:747
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:750
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom_back (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,OO00OOO0O0OOO0OOO [0 ],OOOOO000OO000OO0O [0 ])#line:752
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Connect foot circumference','2, End before reach start point'])#line:756
            cv2 .rectangle (OOO00O0OO00O0O0OO ,(0 ,window_size *2 //3 ),(window_size ,window_size ),(64 ,64 ,64 ),thickness =-1 )#line:758
            cv2 .putText (OOO00O0OO00O0O0OO ,'Click to END & AUTO connect to start point',(0 ,window_size ),cv2 .FONT_HERSHEY_PLAIN ,1.5 ,(255 ,255 ,255 ),1 )#line:759
            O00O000OO0OO0O0O0 ='step5'#line:765
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:766
            OOOO00OOOOO00OO0O =200 #line:767
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:768
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:769
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:770
            cv2 .waitKey ()#line:771
            print ('\n### 後処理')#line:774
            OO000OOO000O0OOO0 =O00000OOOO0O0OOO0 .p /O00O0O0OO0OO000OO #line:777
            print (OO000OOO000O0OOO0 )#line:778
            OOOO0O0OOOOOOO0O0 =((OO000OOO000O0OOO0 [0 ,0 ]-OO000OOO000O0OOO0 [-1 ,0 ])**2 +(OO000OOO000O0OOO0 [0 ,1 ]-OO000OOO000O0OOO0 [-1 ,1 ])**2 )**0.5 #line:780
            for O0O000000O0O0O000 in range (1 ,len (OO000OOO000O0OOO0 )):#line:783
                OOOO0O0OOOOOOO0O0 +=((OO000OOO000O0OOO0 [O0O000000O0O0O000 ,0 ]-OO000OOO000O0OOO0 [O0O000000O0O0O000 -1 ,0 ])**2 +(OO000OOO000O0OOO0 [O0O000000O0O0O000 ,1 ]-OO000OOO000O0OOO0 [O0O000000O0O0O000 -1 ,1 ])**2 )**0.5 #line:784
            print ('c_foot = {}'.format (OOOO0O0OOOOOOO0O0 ))#line:786
        OO000OOOO0OO0OO00 =O00O0O000O000OOOO [1 ]-OOO000OO000O0O000 #line:801
        OOOO000O0O000OOOO =O00O0O000O000OOOO [1 ]#line:802
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:803
        if test :#line:804
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xy',[0 ,OO000OOOO0OO0OO00 ],[0 ,OOOO000O0O000OOOO ])#line:805
        print ('\n### ガースポイント')#line:810
        try :#line:812
            OO00O0000000000OO #line:813
            OO00000OOO00OO00O #line:814
        except NameError :#line:815
            print ('\n### ダウンサンプル')#line:817
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,200000 )#line:819
            print ('\n### 前処理')#line:822
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:825
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom_side (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 )#line:827
            print (O00O0O0OO0OO000OO )#line:828
            O00O0OO0O0OO0OO0O =int ((OOOO000O0O000OOOO *rate2 +OO000OOOO0OO0OO00 *(1 -rate2 ))*O00O0O0OO0OO000OO )#line:831
            OO0OO0OO000OO00O0 =int ((OOOO000O0O000OOOO *rate3 +OO000OOOO0OO0OO00 *(1 -rate3 ))*O00O0O0OO0OO000OO )#line:832
            cv2 .line (OOO00O0OO00O0O0OO ,(O00O0OO0O0OO0OO0O ,0 ),(O00O0OO0O0OO0OO0O ,window_size ),(255 ,255 ,0 ))#line:833
            cv2 .line (OOO00O0OO00O0O0OO ,(OO0OO0OO000OO00O0 ,0 ),(OO0OO0OO000OO00O0 ,window_size ),(255 ,254 ,0 ))#line:834
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Heel girth front','2, Heel girth back'])#line:838
            O00O000OO0OO0O0O0 ='step6'#line:844
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:845
            OOOO00OOOOO00OO0O =1 #line:846
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:847
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:848
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:849
            cv2 .waitKey ()#line:850
            print ('\n### 後処理')#line:853
            OO00O0000000000OO =np .array ([O00O0OO0O0OO0OO0O ,O00000OOOO0O0OOO0 .p [0 ,1 ]])#line:856
            OO00000OOO00OO00O =np .array ([OO0OO0OO000OO00O0 ,window_size //2 ])#line:857
            print (OO00O0000000000OO ,OO00000OOO00OO00O )#line:858
            OO00O0000000000OO [0 ]/=O00O0O0OO0OO000OO #line:861
            OO00O0000000000OO [1 ]=-(OO00O0000000000OO [1 ]-window_size //2 )/O00O0O0OO0OO000OO #line:862
            OO00000OOO00OO00O [0 ]/=O00O0O0OO0OO000OO #line:863
            OO00000OOO00OO00O [1 ]=-(OO00000OOO00OO00O [1 ]-window_size //2 )/O00O0O0OO0OO000OO #line:864
            print ('g_point1 = [{}, {}] #x,z'.format (OO00O0000000000OO [0 ],OO00O0000000000OO [1 ]))#line:865
            print ('g_point2 = [{}, {}] #x,z'.format (OO00000OOO00OO00O [0 ],OO00000OOO00OO00O [1 ]))#line:866
        O0O0OO0O000OO0OO0 =OO00O0000000000OO [1 ]#line:869
        print ('g_step_height = {}'.format (O0O0OO0O000OO0OO0 ))#line:870
        print ('\n### 確認')#line:873
        O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (OOOO0OO00000O0000 ,OO0OOOOOO00O00000 ,20000 )#line:875
        if test :#line:876
            ft .showc (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,'xz',[OO00O0000000000OO [1 ],OO00O0000000000OO [0 ]],[OO00000OOO00OO00O [1 ],OO00000OOO00OO00O [0 ]])#line:877
        print ('\n### ガースの取り出し')#line:891
        O0OOO0O0O00000OO0 =deepcopy (OOOO0OO00000O0000 )#line:894
        O00O00O0000OOO0O0 =deepcopy (OO0OOOOOO00O00000 )#line:895
        O0O0000OOOO0OOOOO =math .atan2 (OO00000OOO00OO00O [1 ]-OO00O0000000000OO [1 ],OO00000OOO00OO00O [0 ]-OO00O0000000000OO [0 ])#line:898
        OOOO0O0OOOOO00000 =math .degrees (O0O0000OOOO0OOOOO )#line:899
        O0O00O0O0OOO00O00 =90 +OOOO0O0OOOOO00000 #line:901
        if O0O00O0O0OOO00O00 >180 :#line:903
            O0O00O0O0OOO00O00 =-360 +O0O00O0O0OOO00O00 #line:904
        if O0O00O0O0OOO00O00 <-180 :#line:905
            O0O00O0O0OOO00O00 =360 -O0O00O0O0OOO00O00 #line:906
        OO00O0000000000OO =ft .rotate_2D_z (OO00O0000000000OO ,theta =O0O00O0O0OOO00O00 )#line:910
        OO00000OOO00OO00O =ft .rotate_2D_z (OO00000OOO00OO00O ,theta =O0O00O0O0OOO00O00 )#line:911
        O0OOO0O0O00000OO0 =ft .rotate_3D_y (O0OOO0O0O00000OO0 ,theta =O0O00O0O0OOO00O00 )#line:912
        OOO0O0O0OO00O0O00 =(O0OOO0O0O00000OO0 [:,0 ]>OO00O0000000000OO [0 ]-2 )*(O0OOO0O0O00000OO0 [:,0 ]<OO00000OOO00OO00O [0 ]+2 )#line:915
        O0OOO0O0O00000OO0 =O0OOO0O0O00000OO0 [OOO0O0O0OO00O0O00 ]#line:916
        O00O00O0000OOO0O0 =O00O00O0000OOO0O0 [OOO0O0O0OO00O0O00 ]#line:917
        O0OOO0O0O00000OO0 [:,2 ]-=OO00000OOO00OO00O [1 ]#line:920
        OO00O0000000000OO [1 ]-=OO00000OOO00OO00O [1 ]#line:921
        OO00000OOO00OO00O [1 ]-=OO00000OOO00OO00O [1 ]#line:922
        if test :#line:924
            ft .showc (O0OOO0O0O00000OO0 ,O00O00O0000OOO0O0 ,'xz',[OO00O0000000000OO [1 ],OO00O0000000000OO [0 ]],[OO00000OOO00OO00O [1 ],OO00000OOO00OO00O [0 ]])#line:925
            ft .showc (O0OOO0O0O00000OO0 ,O00O00O0000OOO0O0 ,'xy')#line:926
        print ('\n### ガース')#line:933
        try :#line:935
            O00OO0O00O0O0O0OO #line:936
        except NameError :#line:937
            print ('\n### ダウンサンプル')#line:939
            O0OO000O00O0000OO ,O00O00O0OOO0OOO00 =ft .down_sample (O0OOO0O0O00000OO0 ,O00O00O0000OOO0O0 ,200000 )#line:941
            print ('\n### 前処理')#line:944
            O00000OOOO0O0OOO0 =cl_class (window_size ,dot_size ,paper_short ,paper_long ,rate1 )#line:947
            OOO00O0OO00O0O0OO ,O00O0O0OO0OO000OO =O00000OOOO0O0OOO0 .window_zoom_back (O0OO000O00O0000OO ,O00O00O0OOO0OOO00 ,0 ,0 )#line:949
            OOO00O0OO00O0O0OO =O00000OOOO0O0OOO0 .put_text (OOO00O0OO00O0O0OO ,['1, Connect girth','2, End before reach start point'])#line:953
            cv2 .rectangle (OOO00O0OO00O0O0OO ,(0 ,window_size *2 //3 ),(window_size ,window_size ),(64 ,64 ,64 ),thickness =-1 )#line:955
            cv2 .putText (OOO00O0OO00O0O0OO ,'Click to END & AUTO connect to start point',(0 ,window_size ),cv2 .FONT_HERSHEY_PLAIN ,1.5 ,(255 ,255 ,255 ),1 )#line:956
            O00O000OO0OO0O0O0 ='step7'#line:962
            cv2 .namedWindow (O00O000OO0OO0O0O0 )#line:963
            OOOO00OOOOO00OO0O =200 #line:964
            OOOOO0O0O000OO00O =pl_class (OOOO00OOOOO00OO0O )#line:965
            cv2 .setMouseCallback (O00O000OO0OO0O0O0 ,O00000OOOO0O0OOO0 .onMouse ,[O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO ,OOOOO0O0O000OO00O ])#line:966
            cv2 .imshow (O00O000OO0OO0O0O0 ,OOO00O0OO00O0O0OO )#line:967
            cv2 .waitKey ()#line:968
            print ('\n### 後処理')#line:971
            OO000OOO000O0OOO0 =O00000OOOO0O0OOO0 .p /O00O0O0OO0OO000OO #line:974
            print (OO000OOO000O0OOO0 )#line:975
            O00OO0O00O0O0O0OO =((OO000OOO000O0OOO0 [0 ,0 ]-OO000OOO000O0OOO0 [-1 ,0 ])**2 +(OO000OOO000O0OOO0 [0 ,1 ]-OO000OOO000O0OOO0 [-1 ,1 ])**2 )**0.5 #line:977
            for O0O000000O0O0O000 in range (1 ,len (OO000OOO000O0OOO0 )):#line:980
                O00OO0O00O0O0O0OO +=((OO000OOO000O0OOO0 [O0O000000O0O0O000 ,0 ]-OO000OOO000O0OOO0 [O0O000000O0O0O000 -1 ,0 ])**2 +(OO000OOO000O0OOO0 [O0O000000O0O0O000 ,1 ]-OO000OOO000O0OOO0 [O0O000000O0O0O000 -1 ,1 ])**2 )**0.5 #line:981
            print ('g_step = {}'.format (O00OO0O00O0O0O0OO ))#line:983
        OO0OOO0OOOOO0OOO0 =['l_foot','w_heel','w_foot','w_len_left','w_len_right','w_len_sum','w_level_left','w_level_right','c_foot','g_step_height','g_step']#line:997
        OO0O000OO0OOO000O =[round (OOO000OO000O0O000 ,1 ),round (O00OOOO0O00000000 ,1 ),round (O00OOOOOOO000OOOO ,1 ),round (OOOOOO0OOOOO0O0O0 ,1 ),round (OO00O00O0O0000OOO ,1 ),round (OOOOOO0OOOOO0O0O0 +OO00O00O0O0000OOO ,1 ),round (OO0O0OOO0OO00O0O0 ,1 ),round (OOOOOOOOOO00OOO00 ,1 ),round (OOOO0O0OOOOOOO0O0 ,1 ),round (O0O0OO0O000OO0OO0 ,1 ),round (O00OO0O00O0O0O0OO ,1 )]#line:1008
        return OO0OOO0OOOOO0OOO0 ,OO0O000OO0OOO000O #line:1010
if __name__ =='__main__':#line:1024
    file ='../test/サンプル太郎/sample.pckl'#line:1041
    file ='https://shoe-craft-terminal.s3.ap-northeast-1.amazonaws.com/サンプル太郎/sample.pckl'#line:1042
    file ='https://shoe-craft-terminal.s3.ap-northeast-1.amazonaws.com/%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E5%A4%AA%E9%83%8E/sample.pckl'#line:1043
    paper_long =297 #line:1045
    paper_short =210 #line:1046
    window_size =1200 #line:1048
    dot_size =1 #line:1050
    cut_height =120 #line:1052
    rate1 =0.18 #line:1054
    rate2 =0.44 #line:1056
    rate3 =0.54 #line:1057
    test =1 #line:1059
    names ,values =vcfoot ().enkaku (file ,paper_long =paper_long ,paper_short =paper_short ,window_size =window_size ,dot_size =dot_size ,cut_height =cut_height ,rate1 =rate1 ,rate2 =rate2 ,rate3 =rate3 ,test =test )#line:1069
    print (names )#line:1072
    print (values )#line:1073
