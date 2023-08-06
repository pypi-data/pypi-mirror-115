import os ,math ,time ,cv2 #line:2
import numpy as np #line:4
import pickle #line:5
import urllib .request #line:6
import urllib .parse #line:7
from PIL import Image #line:8
import matplotlib .pyplot as plt #line:9
np .set_printoptions (threshold =np .inf ,precision =8 ,suppress =True ,floatmode ='maxprec')#line:11
file ='https://shoe-craft-terminal.s3.ap-northeast-1.amazonaws.com/サンプル太郎/sample.pckl'#line:15
s_quote =urllib .parse .quote (file )#line:16
print (s_quote )#line:17
class ft :#line:19
    def __init__ (OO000000O00000000 ):#line:20
        pass #line:21
    def __del__ (O0O0O0OOO0O000OOO ):#line:22
        pass #line:23
    def load_obj (O000OOO000O00OOO0 ):#line:26
        print ('file:\n{}'.format (O000OOO000O00OOO0 ))#line:27
        O0000000OOO000OO0 =[]#line:29
        OO0OOOOOOOOO00OO0 =[]#line:30
        O0O00OO00O0OO00O0 =[]#line:31
        with open (O000OOO000O00OOO0 ,"r")as OOO0O0OOOO0O00O0O :#line:32
            for O000OOO000OO00OO0 in OOO0O0OOOO0O00O0O :#line:33
                OOO00000O000000OO =O000OOO000OO00OO0 .split ()#line:34
                if len (OOO00000O000000OO )==0 :#line:36
                    continue #line:37
                if OOO00000O000000OO [0 ]=='v':#line:38
                    OO000OOOOOOOO0OOO =list (map (float ,OOO00000O000000OO [1 :4 ]))#line:40
                    O0000000OOO000OO0 .append (OO000OOOOOOOO0OOO )#line:41
                    if len (OOO00000O000000OO )==7 :#line:42
                        O00OOO0000OO000OO =list (map (float ,OOO00000O000000OO [4 :7 ]))#line:44
                        OO0OOOOOOOOO00OO0 .append (O00OOO0000OO000OO )#line:45
                if OOO00000O000000OO [0 ]=='f':#line:46
                    OO0O0000O0OO000OO =list (map (int ,OOO00000O000000OO [1 :4 ]))#line:48
                    O0O00OO00O0OO00O0 .append (OO0O0000O0OO000OO )#line:49
        O0000000OOO000OO0 =np .array (O0000000OOO000OO0 )#line:50
        OO0OOOOOOOOO00OO0 =np .array (OO0OOOOOOOOO00OO0 )#line:51
        O0O00OO00O0OO00O0 =np .array (O0O00OO00O0OO00O0 ,int )#line:52
        print ('vertices.shape:\n{}'.format (O0000000OOO000OO0 .shape ))#line:53
        print ('vertexColors.shape:\n{}'.format (OO0OOOOOOOOO00OO0 .shape ))#line:54
        print ('faces.shape:\n{}'.format (O0O00OO00O0OO00O0 .shape ))#line:55
        return O0000000OOO000OO0 ,OO0OOOOOOOOO00OO0 ,O0O00OO00O0OO00O0 #line:56
    def load_pckl (OO0OO00000O0OO00O ):#line:60
        print ('file:\n{}'.format (OO0OO00000O0OO00O ))#line:61
        with open (OO0OO00000O0OO00O ,'rb')as O00O0OOOO00O0OO00 :#line:62
            OO0OOO0OO000OO0O0 ,O0OO00OOO0000OOOO ,O0OO0OO00O00O0OOO =pickle .load (O00O0OOOO00O0OO00 )#line:63
        print ('vertices.shape:\n{}'.format (OO0OOO0OO000OO0O0 .shape ))#line:65
        print ('vertexColors.shape:\n{}'.format (O0OO00OOO0000OOOO .shape ))#line:66
        print ('faces.shape:\n{}'.format (O0OO0OO00O00O0OOO .shape ))#line:67
        return OO0OOO0OO000OO0O0 ,O0OO00OOO0000OOOO ,O0OO0OO00O00O0OOO #line:68
    def load_pckl_url (OOO0O000O0O00000O ):#line:71
        print ('load from cloud')#line:72
        OO0O00OOO0OOOOO00 =OOO0O000O0O00000O .split ('//')[1 ]#line:74
        OO0O00OOO0OOOOO00 =urllib .parse .quote (OO0O00OOO0OOOOO00 )#line:75
        OOO0O000O0O00000O =OOO0O000O0O00000O .split ('//')[0 ]+'//'+OO0O00OOO0OOOOO00 #line:76
        OOOOOO00OOOOOO0OO =urllib .request .Request (OOO0O000O0O00000O )#line:78
        with urllib .request .urlopen (OOOOOO00OOOOOO0OO )as O0OO000OO0OOOOOOO :#line:79
            O0OOO0O0O0OO0OO0O ,O00O000O0O0O0OOO0 ,O0O000O0OOO00OO00 =pickle .load (O0OO000OO0OOOOOOO )#line:80
        print ('vertices.shape:\n{}'.format (O0OOO0O0O0OO0OO0O .shape ))#line:82
        print ('vertexColors.shape:\n{}'.format (O00O000O0O0O0OOO0 .shape ))#line:83
        print ('faces.shape:\n{}'.format (O0O000O0OOO00OO00 .shape ))#line:84
        return O0OOO0O0O0OO0OO0O ,O00O000O0O0O0OOO0 ,O0O000O0OOO00OO00 #line:85
    def down_sample (OO000O00OO00O00OO ,O00000O0OO000OOOO ,O0OOOOOO000O00OO0 ):#line:101
        print ('v.shape:\n{} -> '.format (OO000O00OO00O00OO .shape ),end ='')#line:102
        if len (OO000O00OO00O00OO )>O0OOOOOO000O00OO0 :#line:103
            OO000O00OO00O00OO =OO000O00OO00O00OO [::len (OO000O00OO00O00OO )//O0OOOOOO000O00OO0 ][:O0OOOOOO000O00OO0 ]#line:104
            O00000O0OO000OOOO =O00000O0OO000OOOO [::len (O00000O0OO000OOOO )//O0OOOOOO000O00OO0 ][:O0OOOOOO000O00OO0 ]#line:105
        print ('{}'.format (OO000O00OO00O00OO .shape ))#line:106
        return OO000O00OO00O00OO ,O00000O0OO000OOOO #line:107
    def rotate_3D_x (OOO0O0O000O0OOO0O ,theta =0 ):#line:112
        O0OOO0OOOO00OOOOO =-theta /57.2958 #line:113
        O0O00O0O0000O00OO =np .array ([[1 ,0 ,0 ],[0 ,np .cos (O0OOO0OOOO00OOOOO ),-np .sin (O0OOO0OOOO00OOOOO )],[0 ,np .sin (O0OOO0OOOO00OOOOO ),np .cos (O0OOO0OOOO00OOOOO )]])#line:117
        return np .dot (OOO0O0O000O0OOO0O ,O0O00O0O0000O00OO )#line:118
    def rotate_3D_y (OO0000OO00OOO0O00 ,theta =0 ):#line:120
        OOO0OOOOOO0O0OOO0 =-theta /57.2958 #line:121
        OO0O000OO0O0O00OO =np .array ([[np .cos (OOO0OOOOOO0O0OOO0 ),0 ,np .sin (OOO0OOOOOO0O0OOO0 )],[0 ,1 ,0 ],[-np .sin (OOO0OOOOOO0O0OOO0 ),0 ,np .cos (OOO0OOOOOO0O0OOO0 )]])#line:125
        return np .dot (OO0000OO00OOO0O00 ,OO0O000OO0O0O00OO )#line:126
    def rotate_3D_z (OOO00OO0000O0OOOO ,theta =0 ):#line:128
        OOOO00O0O0OO0OOOO =-theta /57.2958 #line:129
        OOOOOOOO0O0OOOOO0 =np .array ([[np .cos (OOOO00O0O0OO0OOOO ),-np .sin (OOOO00O0O0OO0OOOO ),0 ],[np .sin (OOOO00O0O0OO0OOOO ),np .cos (OOOO00O0O0OO0OOOO ),0 ],[0 ,0 ,1 ]])#line:133
        return np .dot (OOO00OO0000O0OOOO ,OOOOOOOO0O0OOOOO0 )#line:134
    def rotate_2D_z (O00OO0OO000OO00OO ,theta =0 ):#line:137
        OOO0OOO0O00O000OO =+theta /57.2958 #line:138
        OOOOO0OOOOO00O000 =np .array ([[np .cos (OOO0OOO0O00O000OO ),-np .sin (OOO0OOO0O00O000OO )],[np .sin (OOO0OOO0O00O000OO ),np .cos (OOO0OOO0O00O000OO )]])#line:141
        return np .dot (O00OO0OO000OO00OO ,OOOOO0OOOOO00O000 )#line:142
    def show (O000O00O0OO0OOOOO ,dim ='xy',*OO00000OO000000O0 ,save =None ):#line:146
        plt .figure (figsize =(5 ,5 ))#line:147
        OOO0000OO000OO0OO ,O00O0O00000OO00OO ,O0OO000O0O000OO00 =O000O00O0OO0OOOOO [:,0 ],O000O00O0OO0OOOOO [:,1 ],O000O00O0OO0OOOOO [:,2 ]#line:149
        if dim =='xy':#line:150
            plt .scatter (OOO0000OO000OO0OO ,O00O0O00000OO00OO ,c ='k',s =2 )#line:151
        elif dim =='xz':#line:152
            plt .scatter (OOO0000OO000OO0OO ,O0OO000O0O000OO00 ,c ='k',s =2 )#line:153
        elif dim =='yz':#line:154
            plt .scatter (O00O0O00000OO00OO ,O0OO000O0O000OO00 ,c ='k',s =2 )#line:155
        plt .xlabel (dim [0 ]);plt .ylabel (dim [1 ])#line:157
        if len (OO00000OO000000O0 )>0 :#line:159
            OO00000OO000000O0 =np .array (OO00000OO000000O0 )#line:160
            plt .plot (OO00000OO000000O0 [:,0 ],OO00000OO000000O0 [:,1 ],'ro',linewidth =1 )#line:161
        OOOO0O0OOO0OOO00O =np .max (np .array ([[np .max (OOO0000OO000OO0OO )-np .min (OOO0000OO000OO0OO )],[np .max (O00O0O00000OO00OO )-np .min (O00O0O00000OO00OO )],[np .max (O0OO000O0O000OO00 )-np .min (O0OO000O0O000OO00 )]]))#line:163
        if dim =='xy':#line:165
            plt .xlim (np .mean (OOO0000OO000OO0OO )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (OOO0000OO000OO0OO )+OOOO0O0OOO0OOO00O /1.8 )#line:166
            plt .ylim (np .mean (O00O0O00000OO00OO )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (O00O0O00000OO00OO )+OOOO0O0OOO0OOO00O /1.8 )#line:167
        elif dim =='xz':#line:168
            plt .xlim (np .mean (OOO0000OO000OO0OO )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (OOO0000OO000OO0OO )+OOOO0O0OOO0OOO00O /1.8 )#line:169
            plt .ylim (np .mean (O0OO000O0O000OO00 )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (O0OO000O0O000OO00 )+OOOO0O0OOO0OOO00O /1.8 )#line:170
        elif dim =='yz':#line:171
            plt .xlim (np .mean (O00O0O00000OO00OO )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (O00O0O00000OO00OO )+OOOO0O0OOO0OOO00O /1.8 )#line:172
            plt .ylim (np .mean (O0OO000O0O000OO00 )-OOOO0O0OOO0OOO00O /1.8 ,np .mean (O0OO000O0O000OO00 )+OOOO0O0OOO0OOO00O /1.8 )#line:173
        if save !=None :#line:174
            plt .savefig (save )#line:175
        plt .show ()#line:176
        plt .close ()#line:177
    def showc (OO00000O0OOO00OOO ,OO000OOO00O0O0OOO ,dim ='xy',*OOOO0O000O0OO0O00 ,save =None ):#line:179
        plt .figure (figsize =(5 ,5 ))#line:180
        O0O0O000O0O000000 ,O0O000000OOO0O000 ,O0OO0O0OO000O0O0O =OO00000O0OOO00OOO [:,0 ],OO00000O0OOO00OOO [:,1 ],OO00000O0OOO00OOO [:,2 ]#line:182
        if dim =='xy':#line:183
            plt .scatter (O0O0O000O0O000000 ,O0O000000OOO0O000 ,c =OO000OOO00O0O0OOO /255.0 ,s =2 )#line:184
        elif dim =='xz':#line:185
            plt .scatter (O0O0O000O0O000000 ,O0OO0O0OO000O0O0O ,c =OO000OOO00O0O0OOO /255.0 ,s =2 )#line:186
        elif dim =='yz':#line:187
            plt .scatter (O0O000000OOO0O000 ,O0OO0O0OO000O0O0O ,c =OO000OOO00O0O0OOO /255.0 ,s =2 )#line:188
        plt .xlabel (dim [0 ]);plt .ylabel (dim [1 ])#line:190
        if len (OOOO0O000O0OO0O00 )>0 :#line:192
            OOOO0O000O0OO0O00 =np .array (OOOO0O000O0OO0O00 )#line:193
            plt .plot (OOOO0O000O0OO0O00 [:,1 ],OOOO0O000O0OO0O00 [:,0 ],'ro',linewidth =1 )#line:195
        O00OOO00O0OO000OO =np .max (np .array ([[np .max (O0O0O000O0O000000 )-np .min (O0O0O000O0O000000 )],[np .max (O0O000000OOO0O000 )-np .min (O0O000000OOO0O000 )],[np .max (O0OO0O0OO000O0O0O )-np .min (O0OO0O0OO000O0O0O )]]))#line:197
        if dim =='xy':#line:199
            plt .xlim (np .mean (O0O0O000O0O000000 )-O00OOO00O0OO000OO /1.8 ,np .mean (O0O0O000O0O000000 )+O00OOO00O0OO000OO /1.8 )#line:200
            plt .ylim (np .mean (O0O000000OOO0O000 )-O00OOO00O0OO000OO /1.8 ,np .mean (O0O000000OOO0O000 )+O00OOO00O0OO000OO /1.8 )#line:201
        elif dim =='xz':#line:202
            plt .xlim (np .mean (O0O0O000O0O000000 )-O00OOO00O0OO000OO /1.8 ,np .mean (O0O0O000O0O000000 )+O00OOO00O0OO000OO /1.8 )#line:203
            plt .ylim (np .mean (O0OO0O0OO000O0O0O )-O00OOO00O0OO000OO /1.8 ,np .mean (O0OO0O0OO000O0O0O )+O00OOO00O0OO000OO /1.8 )#line:204
        elif dim =='yz':#line:205
            plt .xlim (np .mean (O0O000000OOO0O000 )-O00OOO00O0OO000OO /1.8 ,np .mean (O0O000000OOO0O000 )+O00OOO00O0OO000OO /1.8 )#line:206
            plt .ylim (np .mean (O0OO0O0OO000O0O0O )-O00OOO00O0OO000OO /1.8 ,np .mean (O0OO0O0OO000O0O0O )+O00OOO00O0OO000OO /1.8 )#line:207
        if save !=None :#line:208
            plt .savefig (save )#line:209
        plt .show ()#line:210
        plt .close ()#line:211
class pl_class :#line:223
    def __init__ (O000O00OOO00OO0O0 ,O00O00O00OO0O0O0O ):#line:224
        O000O00OOO00OO0O0 .npoints =O00O00O00OO0O0O0O #line:225
        O000O00OOO00OO0O0 .p =np .empty ((O00O00O00OO0O0O0O ,2 ),dtype =int )#line:226
        O000O00OOO00OO0O0 .count =0 #line:227
    def add (OOOOO00OOO0000O00 ,OO00000OOOO000OO0 ,OOO0OOO0O00O0OOOO ):#line:229
        OOOOO00OOO0000O00 .p [OOOOO00OOO0000O00 .count ,:]=[OO00000OOOO000OO0 ,OOO0OOO0O00O0OOOO ]#line:230
        OOOOO00OOO0000O00 .count +=1 #line:231
class cl_class :#line:234
    def __init__ (O0OO0O0O00O0OOO0O ,O0O0OO0O00OO00O00 ,OO000OO00OO00O0O0 ,OOOO0O0OOO000OO0O ,O000O00O0OOOOOO00 ,O00OO0O000OOO0O0O ):#line:235
        O0OO0O0O00O0OOO0O .window_size =O0O0OO0O00OO00O00 #line:236
        O0OO0O0O00O0OOO0O .dot_size =OO000OO00OO00O0O0 #line:237
        O0OO0O0O00O0OOO0O .h =O0O0OO0O00OO00O00 #line:238
        O0OO0O0O00O0OOO0O .w =O0O0OO0O00OO00O00 #line:239
        O0OO0O0O00O0OOO0O .paper_short =OOOO0O0OOO000OO0O #line:240
        O0OO0O0O00O0OOO0O .paper_long =O000O00O0OOOOOO00 #line:241
        O0OO0O0O00O0OOO0O .rate1 =O00OO0O000OOO0O0O #line:242
        O0OO0O0O00O0OOO0O .p ='a'#line:243
        O0OO0O0O00O0OOO0O .t =0 #line:244
        O0OO0O0O00O0OOO0O .qqq1 =0 #line:245
        O0OO0O0O00O0OOO0O .qqq2 =0 #line:246
    def __del__ (O0O000O0OOOO0OO00 ):#line:248
        pass #line:249
    def window_zoom (OO0O0OO00O00O0O0O ,OOO00OO0O0OOO000O ,OOO00OO0000OOO00O ):#line:251
        OOOO0000OOO000O00 =OOO00OO0O0OOO000O [:,:,[1 ,0 ]]#line:253
        OOOOOO0OO0O0OOO00 =np .zeros ((OO0O0OO00O00O0O0O .window_size ,OO0O0OO00O00O0O0O .window_size ,3 ),'uint8')#line:254
        O00O000OOO0OOO0O0 =OOO00OO0O0OOO000O [:,:,2 ]#line:257
        O00O000OOO0OOO0O0 =np .mean (O00O000OOO0OOO0O0 ,axis =1 )#line:258
        O000O00O00OO000OO =np .max (OOOO0000OOO000O00 [:,:,0 ])#line:260
        OOO0O00O000000O0O =np .max (OOOO0000OOO000O00 [:,:,1 ])#line:261
        O0OOO00OOO0000OO0 =min (OO0O0OO00O00O0O0O .window_size /O000O00O00OO000OO ,OO0O0OO00O00O0O0O .window_size /OOO0O00O000000O0O )#line:265
        OOOO0000OOO000O00 =(OOOO0000OOO000O00 *O0OOO00OOO0000OO0 ).astype (int )#line:267
        print (OOOO0000OOO000O00 .shape )#line:268
        OO0O00O0O00OO000O =np .argsort (O00O000OOO0OOO0O0 )#line:271
        OOOO0000OOO000O00 =OOOO0000OOO000O00 [OO0O00O0O00OO000O ]#line:272
        OOO00OO0000OOO00O =OOO00OO0000OOO00O [OO0O00O0O00OO000O ]#line:273
        O00O00O000000O000 =0 #line:275
        for O0OO0OOOO0000O0O0 in range (len (OOOO0000OOO000O00 [:])):#line:276
            O00O0OO00O000O0OO =OOOO0000OOO000O00 [O0OO0OOOO0000O0O0 ]#line:278
            if np .sum (np .max (O00O0OO00O000O0OO ,axis =0 )-np .min (O00O0OO00O000O0OO ,axis =0 ))>OO0O0OO00O00O0O0O .window_size /50 :#line:281
                continue #line:282
            OO0OOO0O0OOO0O0OO =np .mean (OOO00OO0000OOO00O [O0OO0OOOO0000O0O0 ],axis =0 )#line:284
            OO0OOO0O0OOO0O0OO =tuple ([int (OOOOO000O000O00O0 )for OOOOO000O000O00O0 in OO0OOO0O0OOO0O0OO ])#line:285
            cv2 .fillPoly (OOOOOO0OO0O0OOO00 ,[O00O0OO00O000O0OO ],OO0OOO0O0OOO0O0OO )#line:286
            O00O00O000000O000 +=1 #line:288
            if O00O00O000000O000 %10000 ==0 :#line:289
                print ('/',end ='')#line:290
            if O00O00O000000O000 >=300000 :#line:291
                break #line:292
        print ()#line:293
        OOOOOO0OO0O0OOO00 =cv2 .cvtColor (OOOOOO0OO0O0OOO00 ,cv2 .COLOR_RGB2BGR )#line:295
        cv2 .rectangle (OOOOOO0OO0O0OOO00 ,(OO0O0OO00O00O0O0O .window_size *19 //20 ,0 ),(OO0O0OO00O00O0O0O .window_size ,OO0O0OO00O00O0O0O .window_size //20 ),(64 ,64 ,64 ),thickness =-1 )#line:297
        cv2 .putText (OOOOOO0OO0O0OOO00 ,'Undo',(OO0O0OO00O00O0O0O .window_size *19 //20 ,OO0O0OO00O00O0O0O .window_size //20 ),cv2 .FONT_HERSHEY_PLAIN ,1.0 ,(255 ,255 ,255 ),1 )#line:298
        return OOOOOO0OO0O0OOO00 ,O0OOO00OOO0000OO0 #line:300
    def window_zoom_back (O0O000OO000O000OO ,O00O00O00000OO00O ,OOOO00O0OOO0000O0 ,OO0O0O00000OOO00O ,OOO00O0O00O0000OO ):#line:303
        OOOOOOOOOO0OO0OOO ,OOOOO000000OO0OOO =O00O00O00000OO00O [:,1 ],O00O00O00000OO00O [:,2 ]#line:304
        O000OO00O0000O000 =np .zeros ((O0O000OO000O000OO .window_size ,O0O000OO000O000OO .window_size ,3 ),int )#line:305
        O000O0O0OO0OOO00O =np .max (OOOOOOOOOO0OO0OOO )#line:307
        O000OO0O0O00OOOO0 =O0O000OO000O000OO .window_size /O000O0O0OO0OOO00O #line:310
        OO0OOO0OOOOOOOO0O ,OOO000OO0O0O0O0OO =(OOOOOOOOOO0OO0OOO *O000OO0O0O00OOOO0 ).astype (int ),(OOOOO000000OO0OOO *O000OO0O0O00OOOO0 ).astype (int )#line:311
        OOOOOO0OO0000O0O0 =int (OO0O0O00000OOO00O *O000OO0O0O00OOOO0 )#line:312
        OO00OOOO00OOO00OO =int (OOO00O0O00O0000OO *O000OO0O0O00OOOO0 )#line:313
        OOO000OO0O0O0O0OO =(OOO000OO0O0O0O0OO *-1 )+(O0O000OO000O000OO .window_size //2 )#line:316
        O00OOO0O000O000OO =O0O000OO000O000OO .dot_size #line:318
        for OO0O0OO0OOOOO0OOO in range (len (O00O00O00000OO00O )):#line:319
            if OO0OOO0OOOOOOOO0O [OO0O0OO0OOOOO0OOO ]+O00OOO0O000O000OO <O0O000OO000O000OO .window_size and OOO000OO0O0O0O0OO [OO0O0OO0OOOOO0OOO ]+O00OOO0O000O000OO <O0O000OO000O000OO .window_size :#line:320
                O000OO00O0000O000 [OOO000OO0O0O0O0OO [OO0O0OO0OOOOO0OOO ]-O00OOO0O000O000OO :OOO000OO0O0O0O0OO [OO0O0OO0OOOOO0OOO ]+O00OOO0O000O000OO ,OO0OOO0OOOOOOOO0O [OO0O0OO0OOOOO0OOO ]-O00OOO0O000O000OO :OO0OOO0OOOOOOOO0O [OO0O0OO0OOOOO0OOO ]+O00OOO0O000O000OO ]=OOOO00O0OOO0000O0 [OO0O0OO0OOOOO0OOO ]#line:321
        O000OO00O0000O000 [:,OOOOOO0OO0000O0O0 ,:]=[0 ,255 ,255 ]#line:324
        O000OO00O0000O000 [:,OO00OOOO00OOO00OO ,:]=[0 ,255 ,255 ]#line:325
        O00OOO0O0000OOOOO =Image .fromarray (O000OO00O0000O000 .astype (np .uint8 ))#line:328
        O00OOO0O0000OOOOO =np .array (O00OOO0O0000OOOOO ,dtype =np .uint8 )#line:330
        O00OOO0O0000OOOOO =cv2 .cvtColor (O00OOO0O0000OOOOO ,cv2 .COLOR_RGB2BGR )#line:331
        cv2 .rectangle (O00OOO0O0000OOOOO ,(O0O000OO000O000OO .window_size *19 //20 ,0 ),(O0O000OO000O000OO .window_size ,O0O000OO000O000OO .window_size //20 ),(64 ,64 ,64 ),thickness =-1 )#line:334
        cv2 .putText (O00OOO0O0000OOOOO ,'Undo',(O0O000OO000O000OO .window_size *19 //20 ,O0O000OO000O000OO .window_size //20 ),cv2 .FONT_HERSHEY_PLAIN ,1.0 ,(255 ,255 ,255 ),1 )#line:335
        return O00OOO0O0000OOOOO ,O000OO0O0O00OOOO0 #line:337
    def window_zoom_side (OO0O00OOOOO0OO000 ,OO00OO000O00OO0O0 ,O0OOOOOOOOO00OOO0 ):#line:340
        O0OOO00OOOOOO0000 =OO00OO000O00OO0O0 [:,:,[0 ,2 ]]#line:342
        O0OO0O0OOO0O00000 =np .zeros ((OO0O00OOOOO0OO000 .window_size ,OO0O00OOOOO0OO000 .window_size ,3 ),'uint8')#line:343
        OO00OO0O0OO000O00 =OO00OO000O00OO0O0 [:,:,1 ]#line:346
        OO00OO0O0OO000O00 =np .mean (OO00OO0O0OO000O00 ,axis =1 )#line:347
        O0O000OO00O0000O0 =np .max (O0OOO00OOOOOO0000 [:,:,0 ])#line:349
        O0OO000O00OOO0OO0 =OO0O00OOOOO0OO000 .window_size /O0O000OO00O0000O0 #line:352
        O0OOO00OOOOOO0000 =(O0OOO00OOOOOO0000 *O0OO000O00OOO0OO0 ).astype (int )#line:354
        print (O0OOO00OOOOOO0000 .shape )#line:355
        O0OOO00OOOOOO0000 [:,:,1 ]=(O0OOO00OOOOOO0000 [:,:,1 ]*-1 )+(OO0O00OOOOO0OO000 .window_size //2 )#line:358
        OO0OOO0OO0O00O00O =np .argsort (OO00OO0O0OO000O00 )#line:361
        O0OOO00OOOOOO0000 =O0OOO00OOOOOO0000 [OO0OOO0OO0O00O00O ]#line:362
        O0OOOOOOOOO00OOO0 =O0OOOOOOOOO00OOO0 [OO0OOO0OO0O00O00O ]#line:363
        O000OOO00O0OO0OOO =0 #line:365
        for OOO0OO00O0O0000OO in range (len (O0OOO00OOOOOO0000 [:])):#line:366
            OO00O0O0OO0OO0O00 =O0OOO00OOOOOO0000 [OOO0OO00O0O0000OO ]#line:368
            if np .sum (np .max (OO00O0O0OO0OO0O00 ,axis =0 )-np .min (OO00O0O0OO0OO0O00 ,axis =0 ))>OO0O00OOOOO0OO000 .window_size /50 :#line:371
                continue #line:372
            O00OOOOOOO0O00000 =np .mean (O0OOOOOOOOO00OOO0 [OOO0OO00O0O0000OO ],axis =0 )#line:374
            O00OOOOOOO0O00000 =tuple ([int (OOOOO00000O00O00O )for OOOOO00000O00O00O in O00OOOOOOO0O00000 ])#line:375
            cv2 .fillPoly (O0OO0O0OOO0O00000 ,[OO00O0O0OO0OO0O00 ],O00OOOOOOO0O00000 )#line:376
            O000OOO00O0OO0OOO +=1 #line:378
            if O000OOO00O0OO0OOO %10000 ==0 :#line:379
                print ('/',end ='')#line:380
            if O000OOO00O0OO0OOO >=300000 :#line:381
                break #line:382
        print ()#line:383
        O0OO0O0OOO0O00000 =cv2 .cvtColor (O0OO0O0OOO0O00000 ,cv2 .COLOR_RGB2BGR )#line:385
        cv2 .rectangle (O0OO0O0OOO0O00000 ,(OO0O00OOOOO0OO000 .window_size *19 //20 ,0 ),(OO0O00OOOOO0OO000 .window_size ,OO0O00OOOOO0OO000 .window_size //20 ),(64 ,64 ,64 ),thickness =-1 )#line:387
        cv2 .putText (O0OO0O0OOO0O00000 ,'Undo',(OO0O00OOOOO0OO000 .window_size *19 //20 ,OO0O00OOOOO0OO000 .window_size //20 ),cv2 .FONT_HERSHEY_PLAIN ,1.0 ,(255 ,255 ,255 ),1 )#line:388
        return O0OO0O0OOO0O00000 ,O0OO000O00OOO0OO0 #line:390
    def put_text (O0OO0O0OO0000O0OO ,OO0O0O0OO0OO0000O ,O000OO00OOO00O000 ,right =False ):#line:393
        O0OOO000O00O00000 =20 #line:394
        for OO0000O000OO0O0O0 in range (len (O000OO00OOO00O000 )):#line:395
            if right :#line:396
                O00000OO0OOOOO00O =int (OO0O0O0OO0OO0000O .shape [1 ]/10 *7.5 )#line:397
                cv2 .putText (OO0O0O0OO0OO0000O ,O000OO00OOO00O000 [OO0000O000OO0O0O0 ],(O00000OO0OOOOO00O ,O0OOO000O00O00000 ),cv2 .FONT_HERSHEY_PLAIN ,1.0 ,(255 ,255 ,0 ),1 )#line:398
            else :#line:399
                cv2 .putText (OO0O0O0OO0OO0000O ,O000OO00OOO00O000 [OO0000O000OO0O0O0 ],(5 ,O0OOO000O00O00000 ),cv2 .FONT_HERSHEY_PLAIN ,1.0 ,(255 ,255 ,0 ),1 )#line:400
            O0OOO000O00O00000 +=20 #line:401
        return OO0O0O0OO0OO0000O #line:402
    def gcross (O0OO0OO0000000O00 ,O0OOO0OOO00OO0000 ,O0OO0O00OO00000OO ,OOO000OOO00O0O0O0 ):#line:408
        cv2 .line (O0OOO0OOO00OO0000 ,(O0OO0O00OO00000OO ,0 ),(O0OO0O00OO00000OO ,O0OO0OO0000000O00 .h -1 ),(255 ,255 ,0 ))#line:409
        cv2 .line (O0OOO0OOO00OO0000 ,(0 ,OOO000OOO00O0O0O0 ),(O0OO0OO0000000O00 .w -1 ,OOO000OOO00O0O0O0 ),(255 ,255 ,0 ))#line:410
    def gsquare (O0OO0000OOO00O0O0 ,O0OO00OO00OO0O0OO ,O0O0OOO00O00OO000 ,OO0O00OO0OO00O0OO ,O0OOO00OOOO0000O0 ):#line:412
        OO0O0O0O0OO0OOO00 ,O00O00000OO0OO000 =O0OOO00OOOO0000O0 #line:413
        OO0OO0O0OO00OOOOO =max (abs (O0O0OOO00O00OO000 -OO0O0O0O0OO0OOO00 ),abs (OO0O00OO0OO00O0OO -O00O00000OO0OO000 ))#line:414
        cv2 .rectangle (O0OO00OO00OO0O0OO ,(OO0O0O0O0OO0OOO00 -OO0OO0O0OO00OOOOO ,O00O00000OO0OO000 -OO0OO0O0OO00OOOOO ),(OO0O0O0O0OO0OOO00 +OO0OO0O0OO00OOOOO ,O00O00000OO0OO000 +OO0OO0O0OO00OOOOO ),(255 ,255 ,0 ))#line:415
    def gcircle (OOO00000O0000O00O ,O000OO00000OOOOOO ,OO0OO0OOOOO00O00O ,O0000OOOO0OO0OOOO ):#line:417
        cv2 .circle (O000OO00000OOOOOO ,(OO0OO0OOOOO00O00O ,O0000OOOO0OO0OOOO ),8 ,(255 ,255 ,0 ),1 )#line:418
    def gline (O0OOOO0OO0O00O000 ,O0000OO0000OOO000 ,O0OO0000OO00O0O00 ,OO000OOO000OOOO00 ,O0O0O0000O0O0O00O ):#line:420
        cv2 .line (O0000OO0000OOO000 ,tuple (O0O0O0000O0O0O00O ),(O0OO0000OO00O0O00 ,OO000OOO000OOOO00 ),(255 ,255 ,0 ))#line:421
    def ghline (OO0O0OOO0O0OO0OOO ,OOO00OOO0OOOO00OO ,OO0OO0O00OOO0OOOO ,OOOOOO00O0O0OO000 ):#line:423
        cv2 .line (OOO00OOO0OOOO00OO ,(0 ,OOOOOO00O0O0OO000 ),(OO0O0OOO0O0OO0OOO .w -1 ,OOOOOO00O0O0OO000 ),(255 ,255 ,0 ))#line:424
    def g_heelhline (OO00O0OOOO0OOO000 ,OO0OO0O0O0OO00O0O ,O0O00OOOOOOOO0O0O ,OOO0OOO00000O0OO0 ,O00OOO0OOO000OOOO ,O0O0000O0O0OOOO00 ):#line:426
        OO0O00O0000OO00O0 =int (O00OOO0OOO000OOOO [1 ]*OO00O0OOOO0OOO000 .rate1 +O0O0000O0O0OOOO00 [1 ]*(1 -OO00O0OOOO0OOO000 .rate1 ))#line:427
        cv2 .line (OO0OO0O0O0OO00O0O ,(0 ,OO0O00O0000OO00O0 ),(OO00O0OOOO0OOO000 .w -1 ,OO0O00O0000OO00O0 ),(255 ,255 ,0 ))#line:428
    def gvline (OO0OOO000OO0O0OOO ,OO0O0O0O000O0OO00 ,OO0O000O00OO0OO0O ,O0O0O0OOOOOOO0OOO ):#line:430
        cv2 .line (OO0O0O0O000O0OO00 ,(OO0O000O00OO0OO0O ,0 ),(OO0O000O00OO0OO0O ,OO0OOO000OO0O0OOO .h -1 ),(255 ,255 ,0 ))#line:431
    def gdiagonal (O00OO0OOO00O000OO ,O0O0OO000O0OO0OO0 ,OOOO0O0OOO0000O00 ,O00OO00O0OO000000 ,O0O000OO0O0OO0O00 ):#line:433
        O0O0OOO0O0O0OO000 ,OOOO0O000OOOOO0OO =O0O000OO0O0OO0O00 #line:434
        OOOO0O0OOO0000O00 ,O00OO00O0OO000000 =O00OO00O0OO000000 ,OOOO0O0OOO0000O00 #line:435
        O0O0O00OOO0OOOO0O =math .atan2 (OOOO0O0OOO0000O00 -OOOO0O000OOOOO0OO ,O00OO00O0OO000000 -O0O0OOO0O0O0OO000 )#line:438
        OOOO0O0OOO0O00O0O =math .degrees (O0O0O00OOO0OOOO0O )#line:440
        O000O0OO00OO00O00 =math .atan2 (O00OO0OOO00O000OO .paper_short -0 ,O00OO0OOO00O000OO .paper_long -0 )#line:444
        O0OO0O00OO0OOOOO0 =math .degrees (O000O0OO00OO00O00 )#line:446
        O0OOO0000OO000O00 =OOOO0O0OOO0O00O0O +O0OO0O00OO0OOOOO0 #line:450
        if O0OOO0000OO000O00 >180 :#line:451
            O0OOO0000OO000O00 =-360 +O0OOO0000OO000O00 #line:452
        OOOOO0000O00OO0O0 =math .radians (O0OOO0000OO000O00 )#line:455
        OO00000OO0O0000O0 =((OOOO0O0OOO0000O00 -OOOO0O000OOOOO0OO )**2 +(O00OO00O0OO000000 -O0O0OOO0O0O0OO000 )**2 )**0.5 #line:458
        OO0OO0O00OOO000O0 =(O00OO0OOO00O000OO .paper_long **2 +O00OO0OOO00O000OO .paper_short **2 )**0.5 #line:459
        OOOO0O000OOO0O00O =O00OO0OOO00O000OO .paper_long *(OO00000OO0O0000O0 /OO0OO0O00OOO000O0 )#line:461
        O0O00O0O0OO0OOO0O =O0O0OOO0O0O0OO000 +np .cos (OOOOO0000O00OO0O0 )*OOOO0O000OOO0O00O #line:463
        OO0OOO00000000000 =OOOO0O000OOOOO0OO +np .sin (OOOOO0000O00OO0O0 )*OOOO0O000OOO0O00O #line:464
        cv2 .circle (O0O0OO000O0OO0OO0 ,(int (O0O00O0O0OO0OOO0O ),int (OO0OOO00000000000 )),8 ,(255 ,255 ,0 ),1 )#line:467
        cv2 .circle (O0O0OO000O0OO0OO0 ,(O00OO00O0OO000000 -int (O0O00O0O0OO0OOO0O -O0O0OOO0O0O0OO000 ),OOOO0O0OOO0000O00 -int (OO0OOO00000000000 -OOOO0O000OOOOO0OO )),8 ,(255 ,255 ,0 ),1 )#line:468
    def onMouse (O0O0O00OOOOO000O0 ,OO000O0O0O0O0OOO0 ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,O00O0O000OO0OOO00 ,OOO0OO0O0000O00OO ):#line:471
        O0O0OO0O0O00OO00O ,O0OO000OO0OOOO0O0 ,OO00OOO00O00OO000 =OOO0OO0O0000O00OO #line:472
        if OO000O0O0O0O0OOO0 ==cv2 .EVENT_MOUSEMOVE :#line:475
            OOOOOOOO00000OO0O =np .copy (O0OO000OO0OOOO0O0 )#line:476
            if O0O0OO0O0O00OO00O =='step1':#line:478
                if OO00OOO00O00OO000 .count ==0 :#line:479
                    O0O0O00OOOOO000O0 .gcross (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:480
                if OO00OOO00O00OO000 .count ==1 :#line:481
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),8 ,(0 ,0 ,255 ),1 )#line:482
                    O0O0O00OOOOO000O0 .gsquare (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [0 ])#line:483
            if O0O0OO0O0O00OO00O =='step2':#line:485
                if OO00OOO00O00OO000 .count ==0 :#line:486
                    O0O0O00OOOOO000O0 .gcross (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:487
                if OO00OOO00O00OO000 .count ==1 :#line:488
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),8 ,(0 ,0 ,255 ),1 )#line:489
                    O0O0O00OOOOO000O0 .gcircle (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:490
                    O0O0O00OOOOO000O0 .gdiagonal (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [0 ])#line:491
            if O0O0OO0O0O00OO00O =='step3':#line:493
                if OO00OOO00O00OO000 .count ==0 :#line:494
                    O0O0O00OOOOO000O0 .gcross (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:495
                if OO00OOO00O00OO000 .count ==1 :#line:496
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),8 ,(0 ,0 ,255 ),1 )#line:497
                    O0O0O00OOOOO000O0 .gline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [0 ])#line:498
            if O0O0OO0O0O00OO00O =='step4':#line:500
                if OO00OOO00O00OO000 .count ==0 :#line:501
                    O0O0O00OOOOO000O0 .ghline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:502
                if OO00OOO00O00OO000 .count ==1 :#line:503
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [0 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [0 ,1 ]),(0 ,0 ,255 ))#line:504
                    O0O0O00OOOOO000O0 .ghline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:505
                if OO00OOO00O00OO000 .count ==2 :#line:506
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [0 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [0 ,1 ]),(0 ,0 ,255 ))#line:507
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [1 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [1 ,1 ]),(0 ,0 ,255 ))#line:508
                    O0O0O00OOOOO000O0 .g_heelhline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [0 ],OO00OOO00O00OO000 .p [1 ])#line:509
                    O0O0O00OOOOO000O0 .gvline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:510
                if OO00OOO00O00OO000 .count ==3 :#line:511
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [0 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [0 ,1 ]),(0 ,0 ,255 ))#line:512
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [1 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [1 ,1 ]),(0 ,0 ,255 ))#line:513
                    O00OO0O0O00O0O0OO =int (OO00OOO00O00OO000 .p [0 ,1 ]*O0O0O00OOOOO000O0 .rate1 +OO00OOO00O00OO000 .p [1 ,1 ]*(1 -O0O0O00OOOOO000O0 .rate1 ))#line:514
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple ((OO00OOO00O00OO000 .p [2 ,0 ],O00OO0O0O00O0O0OO )),8 ,(0 ,0 ,255 ),1 )#line:515
                    O0O0O00OOOOO000O0 .g_heelhline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [0 ],OO00OOO00O00OO000 .p [1 ])#line:516
                    O0O0O00OOOOO000O0 .gvline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:517
                if OO00OOO00O00OO000 .count ==4 :#line:518
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [0 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [0 ,1 ]),(0 ,0 ,255 ))#line:519
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [1 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [1 ,1 ]),(0 ,0 ,255 ))#line:520
                    O00OO0O0O00O0O0OO =int (OO00OOO00O00OO000 .p [0 ,1 ]*O0O0O00OOOOO000O0 .rate1 +OO00OOO00O00OO000 .p [1 ,1 ]*(1 -O0O0O00OOOOO000O0 .rate1 ))#line:521
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple ((OO00OOO00O00OO000 .p [2 ,0 ],O00OO0O0O00O0O0OO )),8 ,(0 ,0 ,255 ),1 )#line:522
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple ((OO00OOO00O00OO000 .p [3 ,0 ],O00OO0O0O00O0O0OO )),8 ,(0 ,0 ,255 ),1 )#line:523
                    cv2 .line (OOOOOOOO00000OO0O ,(OO00OOO00O00OO000 .p [2 ,0 ],O00OO0O0O00O0O0OO ),(OO00OOO00O00OO000 .p [3 ,0 ],O00OO0O0O00O0O0OO ),(0 ,0 ,255 ))#line:524
                    O0O0O00OOOOO000O0 .gcross (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:525
                if OO00OOO00O00OO000 .count ==5 :#line:526
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [0 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [0 ,1 ]),(0 ,0 ,255 ))#line:527
                    cv2 .line (OOOOOOOO00000OO0O ,(0 ,OO00OOO00O00OO000 .p [1 ,1 ]),(O0O0O00OOOOO000O0 .w -1 ,OO00OOO00O00OO000 .p [1 ,1 ]),(0 ,0 ,255 ))#line:528
                    O00OO0O0O00O0O0OO =int (OO00OOO00O00OO000 .p [0 ,1 ]*O0O0O00OOOOO000O0 .rate1 +OO00OOO00O00OO000 .p [1 ,1 ]*(1 -O0O0O00OOOOO000O0 .rate1 ))#line:529
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple ((OO00OOO00O00OO000 .p [2 ,0 ],O00OO0O0O00O0O0OO )),8 ,(0 ,0 ,255 ),1 )#line:530
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple ((OO00OOO00O00OO000 .p [3 ,0 ],O00OO0O0O00O0O0OO )),8 ,(0 ,0 ,255 ),1 )#line:531
                    cv2 .line (OOOOOOOO00000OO0O ,(OO00OOO00O00OO000 .p [2 ,0 ],O00OO0O0O00O0O0OO ),(OO00OOO00O00OO000 .p [3 ,0 ],O00OO0O0O00O0O0OO ),(0 ,0 ,255 ))#line:532
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [4 ]),8 ,(0 ,0 ,255 ),1 )#line:533
                    O0O0O00OOOOO000O0 .gline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [4 ])#line:534
            if O0O0OO0O0O00OO00O in ['step5','step7']:#line:537
                cv2 .line (OOOOOOOO00000OO0O ,(0 ,O0O0O00OOOOO000O0 .window_size //2 ),(O0O0O00OOOOO000O0 .w -1 ,O0O0O00OOOOO000O0 .window_size //2 ),(255 ,255 ,0 ))#line:538
                if O0O0O00OOOOO000O0 .t >0 :#line:540
                    cv2 .line (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),tuple (OO00OOO00O00OO000 .p [OO00OOO00O00OO000 .count -2 ]),(0 ,0 ,255 ))#line:541
                    OO00OOO00O00OO000 .npoints =OO00OOO00O00OO000 .count #line:542
                    time .sleep (1 )#line:543
                elif OO00OOO00O00OO000 .count >0 and O00OOO00000O00O00 <=(O0O0O00OOOOO000O0 .window_size *2 //3 ):#line:545
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),8 ,(0 ,0 ,255 ),1 )#line:546
                    for OO0OOO00O0O00O0OO in range (1 ,OO00OOO00O00OO000 .count ):#line:547
                        cv2 .line (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [OO0OOO00O0O00O0OO -1 ]),tuple (OO00OOO00O00OO000 .p [OO0OOO00O0O00O0OO ]),(0 ,0 ,255 ))#line:548
                    O0O0O00OOOOO000O0 .gline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ,OO00OOO00O00OO000 .p [OO00OOO00O00OO000 .count -1 ])#line:549
                elif OO00OOO00O00OO000 .count >0 and O00OOO00000O00O00 >(O0O0O00OOOOO000O0 .window_size *2 //3 ):#line:551
                    cv2 .circle (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [0 ]),8 ,(0 ,0 ,255 ),1 )#line:552
                    for OO0OOO00O0O00O0OO in range (1 ,OO00OOO00O00OO000 .count ):#line:553
                        cv2 .line (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [OO0OOO00O0O00O0OO -1 ]),tuple (OO00OOO00O00OO000 .p [OO0OOO00O0O00O0OO ]),(0 ,0 ,255 ))#line:554
                    cv2 .line (OOOOOOOO00000OO0O ,tuple (OO00OOO00O00OO000 .p [OO00OOO00O00OO000 .count -1 ]),tuple (OO00OOO00O00OO000 .p [0 ]),(255 ,255 ,0 ))#line:555
            if O0O0OO0O0O00OO00O =='step6':#line:557
                if O0O0O00OOOOO000O0 .qqq1 ==0 :#line:558
                    for OO0OOO00O0O00O0OO in range (O0O0O00OOOOO000O0 .w ):#line:560
                        if np .sum (np .abs (O0OO000OO0OOOO0O0 [O00OOO00000O00O00 ,OO0OOO00O0O00O0OO ]-np .array ([255 ,255 ,0 ],int )))==0 :#line:561
                            O0O0O00OOOOO000O0 .qqq1 =OO0OOO00O0O00O0OO #line:562
                            break #line:563
                    for OO0OOO00O0O00O0OO in range (O0O0O00OOOOO000O0 .w ):#line:564
                        if np .sum (np .abs (O0OO000OO0OOOO0O0 [O00OOO00000O00O00 ,OO0OOO00O0O00O0OO ]-np .array ([255 ,254 ,0 ],int )))==0 :#line:565
                            O0O0O00OOOOO000O0 .qqq2 =OO0OOO00O0O00O0OO #line:566
                            break #line:567
                O0O0O00OOOOO000O0 .ghline (OOOOOOOO00000OO0O ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:569
                cv2 .line (OOOOOOOO00000OO0O ,(O0O0O00OOOOO000O0 .qqq1 ,O00OOO00000O00O00 ),(O0O0O00OOOOO000O0 .qqq2 ,O0O0O00OOOOO000O0 .window_size //2 ),(255 ,255 ,0 ))#line:570
            cv2 .imshow (O0O0OO0O0O00OO00O ,OOOOOOOO00000OO0O )#line:572
        if OO000O0O0O0O0OOO0 ==cv2 .EVENT_LBUTTONDOWN :#line:575
            if O0O0O00OOOOO000O0 .window_size *19 //20 <OOO000O00OO0OOO00 <O0O0O00OOOOO000O0 .window_size and 0 <O00OOO00000O00O00 <O0O0O00OOOOO000O0 .window_size //20 :#line:578
                if OO00OOO00O00OO000 .count ==0 :#line:579
                    pass #line:580
                else :#line:581
                    OO00OOO00O00OO000 .count -=1 #line:582
                    OO00OOO00O00OO000 .p [OO00OOO00O00OO000 .count ,:]==np .empty (2 ,dtype =int )#line:583
            else :#line:587
                OO00OOO00O00OO000 .add (OOO000O00OO0OOO00 ,O00OOO00000O00O00 )#line:589
                print ('pointlist[{}] = ({}, {})'.format (OO00OOO00O00OO000 .count -1 ,OOO000O00OO0OOO00 ,O00OOO00000O00O00 ))#line:590
                if O0O0OO0O0O00OO00O in ['step5','step7']:#line:592
                    if O00OOO00000O00O00 >(O0O0O00OOOOO000O0 .window_size *2 //3 ):#line:593
                        O0O0O00OOOOO000O0 .t =time .time ()#line:595
        if OO00OOO00O00OO000 .count ==OO00OOO00O00OO000 .npoints :#line:600
            cv2 .destroyWindow (O0O0OO0O0O00OO00O )#line:601
            if O0O0OO0O0O00OO00O in ['step5','step7']:#line:602
                O0O0O00OOOOO000O0 .p =OO00OOO00O00OO000 .p [:OO00OOO00O00OO000 .count -1 ]#line:603
            else :#line:604
                O0O0O00OOOOO000O0 .p =OO00OOO00O00OO000 .p #line:605
if __name__ =='__main__':#line:609
    pass #line:610
