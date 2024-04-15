import cv2
from PIL import Image


import OpenPifPafTools.OpenPifPafGetData as oppgd


'''
Clf.is_pil_patient
'''
def my_func(Clf,OppBoxPred,frame,label_list=['Negative','Neutro','Pain','Positive']):
    img_tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
    pil_im = Image.fromarray(img_tmp);
    
    height, width, channels = frame.shape
    
    annotation, gt_anns, image_meta = OppBoxPred.pil_image(pil_im);
    
    for annot in annotation: 
        (xi,yi,xo,yo)=oppgd.get_body_bounding_rectangle(annot.data,factor=1.0);
        xi=int(xi);        yi=int(yi);
        xo=int(xo);        yo=int(yo);
        
        if xo<0:
            xo=0;
        if xo>=width:
            xo=width-1;
        if yo<0:
            yo=0;
        if yo>=height:
            yo=height-1;
        
        color=(0,255,0);
        thickness=2;
        
        pil_crop=pil_im.crop((xi,yi,xo,yo));
        
        texto=label_list[Clf.is_pil_patient(pil_crop)];
        
        frame = cv2.putText(  frame,
                              texto,
                              org = (int(xi), int((yi+yo)/4)),
                              fontFace = cv2.FONT_HERSHEY_DUPLEX,
                              fontScale = 2.0,
                              color = (255, 0, 0),
                              thickness = thickness
                            )
        
        cv2.rectangle(frame,(xi,yi),(xo,yo),color,thickness);
    return frame;
