% finally need to use matlab to plot the migration curves. 

load burstinfo;
x=burstinfo;

diffusive=x(:,9);
index=x(:,1);

itype=2;

for i=1:length(index)
	file=strcat('xyz_',num2str(index(i)));
	if (index(i)<10) 
		file=strcat('xyz_0',num2str(index(i)));
	end
	a=load(file);
	diffusion=diffusive(i);
	etime=date2mjd(a(:,1),a(:,2),a(:,3),a(:,4),a(:,5),a(:,6)); % unit is days
	if (itype==2) 
		emag=a(:,7);
		elat=a(:,8);
		elon=a(:,9);
		edep=a(:,10);
	end
	
	depmed(i)=median(edep);
	depmean(i)=mean(edep);

	sindex=find(etime==min(etime));
	etime=(etime-min(etime));
	slat=elat(sindex);
	slon=elon(sindex);
	sdep=edep(sindex);
	aspect=cos(median(elat)*pi/180.);
	delkm=111.19;
	
	dist=sqrt(((elat-slat)*111.19).^2+((elon-slon)*111.19*aspect).^2+(edep-sdep).^2);

% the unit of diffusion is m^2/s. 
% distpred=sqrt(4*pi*D*t);
	distp=min(dist):0.01:max(dist)+0.5;
	ptime=(distp*1000).^2/(4*pi*diffusion*3600*24);
	
	diffusion1=diffusion/2;
	diffusion2=diffusion/5;
	diffusion3=diffusion*2;
	diffusion4=diffusion*5;
	
	ptime1=(distp*1000).^2/(4*pi*diffusion1*3600*24);
	ptime2=(distp*1000).^2/(4*pi*diffusion2*3600*24);
	ptime3=(distp*1000).^2/(4*pi*diffusion3*3600*24);
	ptime4=(distp*1000).^2/(4*pi*diffusion4*3600*24);
	%distp1=sqrt(4*pi*diffusion1*ptime*3600*24)/1000;
	%distp2=sqrt(4*pi*diffusion2*ptime*3600*24)/1000;
	%distp3=sqrt(4*pi*diffusion3*ptime*3600*24)/1000;
	%distp4=sqrt(4*pi*diffusion4*ptime*3600*24)/1000;
	
	figure();
	plot(etime,dist,'k.',ptime,distp,'r',ptime1,distp,'c-.',ptime2,distp,'m-.',ptime3,distp,'b-.',ptime4,distp,'g-.');
	xlim([min(etime),max(etime)]);
	ylim([min(dist),max(dist)+0.1]);
	xlabel('time /days');
	ylabel('distance /km');
	if (index(i)<10) 
		saveas(gcf,strcat('swarm_0',num2str(index(i)),'.pdf'));
	else
		saveas(gcf,strcat('swarm_',num2str(index(i)),'.pdf'));
	end
end

figure();
plot(depmed,diffusive,'.',depmean,diffusive,'r.');
