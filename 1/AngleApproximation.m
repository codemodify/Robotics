clc;
close all;clear all;
load maskc_s maskc_s % loading the mask for detecting approximate fingertip nominies
%load maskc_d maskc_d  %loading mask for detecting initial orientation of each finger

maskc=maskc_s;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

th=-150.0; %threshold for approximate fingertip detect
% cam = videoinput('winvideo',1,'I420_160x120');

imageWidth = 320;
imageHeight = 240;

% YUY2_160x120
% YUY2_176x144
% YUY2_320x240
% YUY2_352x288
% YUY2_640x480
% YUY2_1280x720

cam = videoinput('winvideo',1,'YUY2_320x240');
cam.returnedcolorspace='rgb';
triggerconfig(cam, 'manual');
set(cam,'FramesPerTrigger',1);
set(cam,'TriggerRepeat',Inf);
fh = figure;
start(cam)  
FirstFrame=1;
PSF = fspecial('average');

% Stup TCP server
% ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
%tcpServer = tcpip('127.0.0.1',55000,'NetworkRole','Server');
%fopen(tcpServer);
%set(t, 'OutputEmptyFcn', {'dispcallback'});

% disp('finger1 finger2 finger3 finger4 finger5')
while(1)
    trigger(cam);
    NerakImage = getdata(cam);
%tic
    imh=rgb2hsv(NerakImage);

    %%%%%%% Skin Filter %%%%%%%%%%%
    j=find(imh(:,:,1)<.05 & imh(:,:,2)>.17);
    k=find(imh(:,:,1)<.1 & imh(:,:,2)>.3);
    i=find(imh(:,:,1)>.9 & imh(:,:,2)>.15);
    %%%%%%%%%%%%%%%%%%%%%%
    imf=zeros(imageHeight,imageWidth);
    imf(i)=ones(size(i));
    imf(j)=ones(size(j));
    imf(k)=ones(size(k));

    %%%%%%%% averaging and smoothing %%%%%%%%%%%%%
    imib = imfilter(imf,PSF,'symmetric','conv');
    krn_image=zeros(imageHeight,imageWidth);
    Neraksabi=zeros(imageHeight,imageWidth);
    krn_image(imib>.5)=1; % binary silhouttee of input image
  
    %%%%%%%%%%%% Finding the Biggest BLOB %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[k num]=bwlabel(krn_image,8); 
 j=find(k==1);
for i=1:num-1
   if(length(j)<length(find(k==i+1)))
        j=find(k==i+1);
    end
end
Neraksabi(j)=1;
%%%%%%%%%%%%%%%%%%% End of Finding the Biggest BLOB %%%%%%%%%%%%%%%%%%%%%%%
  % figure,imshow(Neraksabi);   
%calculating integral image

    imib(1,1)=Neraksabi(1,1);
    rsum=0;
    for i=2:size(Neraksabi,1)
        for j=1:size(Neraksabi,2)
            if j==1
                rsum=0;
            end
            rsum=rsum+Neraksabi(i,j);
            imib(i,j)=imib(i-1,j)+rsum;
        end
    end
    %imib contains the integral image or summed area table of the input image
    
    %calculating center of the palm
    imtm=Neraksabi;
    ms=[40,40];
    z=1;cen=zeros(5000,2);
    for i=1:size(imib,1)-ms(1)
        for j=1:size(imib,2)-ms(2)
            if imib(i,j)+imib(i+ms(1)-1,j+ms(2)-1)-imib(i,j+ms(2)-1)-imib(i+ms(1)-1,j)>1479
                imtm(i:i++ms(1)-1,j:j+ms(2)-1)=zeros(ms(1),ms(2));
                cen(z,:)=[i+(round(ms(1)/2)),j+(round(ms(2)/2))];
                z=z+1;
            end
        end
    end
    
    %calculating mean of all the central points obtained above
    i=find(cen>0);
    c1=round(2*sum(cen(:,1)/length(i)));
    c2=round(2*sum(cen(:,2)/length(i)));
   if (any(isnan(c1))||any(isnan(c2)))


%     if(isNaN(uint8(c1))==1||isNaN(uint8(c2))==1)
        continue
    end
    NerakImage(c1,c2,:)=[255 255 0];
%%%%%%%%%%%%% End of Centre of Palm Detection %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
    % cen_m contains the center of the palm
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%% Calculating approximate fingertip location %%%%%%%%%%%%
    ms=size(maskc);
    maskv=zeros(size(Neraksabi,1)-ms(1),size(Neraksabi,2)-ms(2));
    % masking the Neraksabi with mask %
    for i=1:size(Neraksabi,1)-ms(1)
        for j=1:size(Neraksabi,2)-ms(2)
            if imtm(i+10,j+10)==1
                maskv(i,j)=sum(sum(maskc.*Neraksabi(i:i+ms(1)-1,j:j+ms(2)-1)));
            end
        end
    end
    % maskv stores the masked values of the image %
    ind=find(imtm(11:110,11:150)==0);
    maskv(ind)=-500;

    % setting the threshold for approximate fingertip nominees
    mask_cod=zeros(size(maskv));
    mask_cod(maskv>th)=1;
    % selecting the group with maximum no. of nominees

    [L,num] = bwlabel(mask_cod,8);
%o=num
    mask_cod=zeros(size(mask_cod));
    for i=1:num
        if length(find(L==i))>1
            [r,c] = find(L==i);
            mask_cod(round(mean(r)),round(mean(c)))=1;
        end
    end
    % mask_cod contains the approximate fingertip location of the opened
    % fingers
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %calculating the fingertip values wrt the origional image
    [r,c]=find(mask_cod==1);
    r=r+10;
    c=c+10;
    
    % r and c contains the approximate row and coloumn values of the opened fingertips
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%% Calculating actual fingertip location %%%%%%%%%%%%
             %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dist=0;
 if ~isempty(r)
         for k=1:length(r)
                theta=atan2((r(k)-c1),(c(k)-c2));% initial angular orientation of the finger
                R=.25;
                while (1)
                    ii=round(r(k)+R*sin(theta));
                    jj=round(c(k)+R*cos(theta));
                    if (any(isnan(ii))||any(isnan(jj))||(ii<1)||(jj<1))

                        break;
                    end
                % moving in the direction opposite to theta towards the end of the finger
                % till we reach the end of the finger.... hurray its the fingertip :)
                    fr=ii;fc=jj;
                    R=R+.25;
                    if ii>imageHeight || jj>imageWidth
                        break;
                    end
                    if Neraksabi(ii,jj)==0
                        break;
                    end



                end
                r(k)=fr;
                c(k)=fc;
                NerakImage(r(k),c(k),:)=[255 255 255];
                dist(k)=sqrt((c1-r(k))^2+(c2-c(k))^2); %#ok<AGROW>
         end


 end 
 if (dist==0)
     continue
 end
 if length(dist)<=5
     if FirstFrame==1
         y=dist;
         if numel(y)==5
             FirstFrame=0;
         end
     end
     for i=1:numel(dist)
        if y(i)<dist(i)
            y(i)=dist(i);
        end
     end
     for i=1:numel(dist)
        Angl(i)=round(90+((dist(i)-2*y(i)/5))*90/(3*y(i)/5)); %#ok<AGROW>
     end
     imshow(NerakImage)
     
     fingerData = num2str(Angl);
     set(fh,'name',fingerData)
 
     % Write data to file
     % ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
     fileName = 'c:\Users\Nicolae\Temp\fingerdata.txt';
     fileDescriptor = fopen(fileName, 'w');
     fprintf(fileDescriptor, fingerData);
     fclose(fileDescriptor);

 end
 imshow(NerakImage)

 % Send data over network
 % ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
 % fwrite(tcpipServer,data(:),'double');
 %str = sprintf('%d %d %d %d %d %d %d %d\n', r, c, c1, c2, fr, fc, ii, jj);
 %fprintf(tcpServer, str, 'async')
 
 clearvars dist NerakImage r c c1 c2 fr fc ii jj ;

%toc
end

% Cleanup TCP server
% ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
%fclose(tcpServer);


% %%%%%%%%%%% main end %%%%%%%%%%%%%%%%%%%