% view_test.m


% Continue where we left off..
% ray_test
gauss_ray

w = 7;				% view plane width
dis = -7;			% distance of image capture plane from viewpoint

image_w = 1024;

p_radius = 3;

view_plane = [ w/2  0  w/2;
			   w/2  0 -w/2;
			  -w/2  0  w/2;
			  -w/2  0 -w/2;
			   0 dis 0 ];	% Origin here so that the transformation is 'wholesale'

view_tri = [1 2 4;
			1 3 4];

% inherit figure axes from ray_test
figure(2);
hold on;

% view(90,0)		% side view
% view(35,-20)		% low angle

view_plane = trans_mat2(view_plane,0,-25,0);
viewpoint = view_plane(5,:);

% Determine corners
plot3(view_plane(1,1),view_plane(1,2),view_plane(1,3),'^')	% 1: Upper Right
plot3(view_plane(2,1),view_plane(2,2),view_plane(2,3),'*')	% 2: Lower Right
plot3(view_plane(3,1),view_plane(3,2),view_plane(3,3),'s')	% 3: Upper Left
plot3(view_plane(4,1),view_plane(4,2),view_plane(4,3),'+')	% 4: Lower Left

UL = view_plane(3,:);
UR = view_plane(1,:);
LR = view_plane(2,:);
LL = view_plane(4,:);

trimesh(view_tri,view_plane(:,1),view_plane(:,2),view_plane(:,3));
plot3(viewpoint(1),viewpoint(2),viewpoint(3),'ro');

text(viewpoint(1),viewpoint(2),viewpoint(3),'viewpoint');


view_uv = [];

% Generate secondary rays
for i = 1:length(intsc)
	disp(sprintf('Tracing view ray %d/%d (%.2f %%) \n',i,total_rays,100*i/total_rays))

	[fl,u,v,t] = rayQuad(intsc(i,:),viewpoint - intsc(i,:),UL,UR,LR,LL);
	view_uv = [ view_uv; 
				u v];
	if plot_bool == 1
		k = (linspace(0,t,2))';
		vray = f_param_ray(k,viewpoint - intsc(i,:),intsc(i,:));
		plot3(vray(:,1),vray(:,2),vray(:,3),'r');

		int_point = vray(end,:);		% get the intersection point
		plot3(int_point(1),int_point(2),int_point(3),'^');

		% Test u and v 					had to invert U vs L for some reason
		int_point = (1-u)*(1-v)*UL ...
				  + u*(1-v)*UR ...
				  + u*v*LR	 ...
				  + (1-u)*v*LL;

		plot3(int_point(1),int_point(2),int_point(3),'+');
	end
end

% [ix,iy] = meshgrid(lerps);


% Image munging
view_uv = floor(view_uv * image_w);

% Initialize a black image
view_im = uint8(255*ones(image_w,image_w,3));
% view_im(:,:,2) = ones(image_w,image_w);
figure(3);

for i = 1:size(view_uv,1)		% Light selected pixels 
	u = view_uv(i,2);
	v = view_uv(i,1);
	if exist('data') > 0
		view_im([u-p_radius:u+p_radius],[v-p_radius:v+p_radius],1) = uint8(data(i,1));
		view_im([u-p_radius:u+p_radius],[v-p_radius:v+p_radius],2) = uint8(data(i,2));
		view_im([u-p_radius:u+p_radius],[v-p_radius:v+p_radius],3) = uint8(data(i,3));
	else
		view_im([u-p_radius:u+p_radius],[v-p_radius:v+p_radius],:) = 0;
	end%if
end

image(view_im);
axis square
imwrite(view_im,'sim_out.png');

if exist('data') > 0
	h = figure(1);
	set(h, 'PaperPosition', [0 0 5 5]); 
	set(h, 'PaperSize', [5 5]);
	saveas(h,'gaussian','pdf')

	h = figure(2);
	set(h, 'PaperPosition', [0 0 15 15]); 
	set(h, 'PaperSize', [15 15]);
	saveas(h,'ray_diagram','pdf')

	h = figure(4);
	set(h, 'PaperPosition', [0 0 5 5]); 
	set(h, 'PaperSize', [5 5]);
	saveas(h,'sampled_pixels','png')

end




