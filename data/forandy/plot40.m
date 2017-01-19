load xyz_40_1;
b=xyz_40_1;
d1=0.008;
emag1=b(:,7);
elat1=b(:,8);
elon1=b(:,9);
edep1=b(:,10);
etime1=date2mjd(b(:,1),b(:,2),b(:,3),b(:,4),b(:,5),b(:,6));
sindex=find(etime1==min(etime1));
est1=etime1(sindex);
etime1=etime1-min(etime1);
slat1=elat1(sindex);
slon1=elon1(sindex);
sdep1=edep1(sindex);

load xyz_40_2;
c=xyz_40_2;
d2=0.05;
emag2=c(:,7);
elat2=c(:,8);
elon2=c(:,9);
edep2=c(:,10);
etime2=date2mjd(c(:,1),c(:,2),c(:,3),c(:,4),c(:,5),c(:,6));
sindex=find(etime2==min(etime2));
est2=etime2(sindex);
etime2=etime2-min(etime2);
slat2=elat2(sindex);
slon2=elon2(sindex);
sdep2=edep2(sindex);

elat=[elat1; elat2];
elon=[elon1; elon2];
edep=[edep1; edep2];
index1=1:length(elat1);
index2=(1:length(elat2))+length(elat1);
d0=0.04;
a=[b;c];
etime=date2mjd(a(:,1),a(:,2),a(:,3),a(:,4),a(:,5),a(:,6));
sindex=find(etime==min(etime));
aspect=cos(median(elat)*pi/180.);
etime=etime-min(etime);
slat=elat(sindex);
slon=elon(sindex);
sdep=edep(sindex);
delkm=111.19;
dist=sqrt(((elat-slat)*111.19).^2+((elon-slon)*111.19*aspect).^2+(edep-sdep).^2);
distp=min(dist):0.01:max(dist);
ptime=(distp*1000).^2/(4*pi*d0*3600*24);

dist1=sqrt(((elat1-slat1)*111.19).^2+((elon1-slon1)*111.19*aspect).^2+(edep1-sdep1).^2);
distp1=min(dist1):0.01:max(dist1);
ptime1=(distp1*1000).^2/(4*pi*d1*3600*24);

dist2=sqrt(((elat2-slat2)*111.19).^2+((elon2-slon2)*111.19*aspect).^2+(edep2-sdep2).^2);
distp2=min(dist2):0.01:max(dist2);
ptime2=(distp2*1000).^2/(4*pi*d2*3600*24);

subplot(2,2,1);
latlim=[min(elat),max(elat)];
lonlim=[min(elon),max(elon)];
h=usamap(latlim,lonlim);
setm(h,'mlinelocation',0.001);
setm(h,'plinelocation',0.001);
setm(h,'mlabellocation',0.005);
setm(h,'plabellocation',0.006);
plotm(elat1,elon1,'r.');
plotm(elat2,elon2,'k.');

subplot(2,2,2);
plot(etime(index1),dist(index1),'r.',ptime,distp);
hold on;
plot(etime(index2),dist(index2),'k.');
xlim([min(etime),max(etime)]);
xlabel('time/hour');
ylabel('distance/km');

subplot(2,2,3);
plot(etime1,dist1,'r.',ptime1,distp1,'r');
xlim([min(etime1),max(etime1)]);
xlabel('time/hour');
ylabel('distance/km');

subplot(2,2,4);
plot(etime2,dist2,'k.',ptime2,distp2,'k');
xlabel('time/hour');
ylabel('distance/km');
