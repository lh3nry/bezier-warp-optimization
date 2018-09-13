% gauss_ray.m
close all; clear all;

win_size = 550;
num_samples = 25;


test_orig = imread('colour_test.png');
% Grab the width dimension of the image that was loaded
w_orig = size(test_orig,1);
% Allowance for control points to 'exceed' axes bounds (doesn't work)
% need to see how to tune imshow
padding = 100;

test_pad = padarray(test_orig,[padding padding],'both');
w_pad = size(test_pad,1);


% Generate uniform control point grid
cp_grid = floor(linspace(padding,w_orig+padding,4));

[Cx, Cy] = meshgrid(cp_grid);

Cx = reshape(Cx,16,1);
Cy = reshape(Cy,16,1);

% Draw samples
r_samples = gauss_samples(Cx,Cy,w_pad,w_orig/2,padding,num_samples);
% r_samples = gauss_samples(Cx([5 6 7]),Cy([5 6 7]),w_pad,w_orig/2,padding,num_samples);
total_rays = length(r_samples);

% Plot gaussian sample points
h = figure(1);
plot(Cx,Cy,'go')
axis square
xlim([0 w_pad]);
ylim([0 w_pad]);
hold on;

plot(r_samples(:,2),r_samples(:,1),'r+');
set(gca, 'YDir', 'reverse');
set(h, 'Position', [0 0 win_size win_size]);


% Make blank image
gauss_im = uint8(zeros(w_pad,w_pad,3));

% Pixel blobbing
blob_bool = 1;
rad = 3;

for i = 1:size(r_samples,1)
	u = r_samples(i,1);
	v = r_samples(i,2);

	% matlab 1-indexing conversion
	if u == 0
		u = 1;
	end
	if v == 0
		v = 1;
	end

	if blob_bool == 1 && u>rad+1 && v>rad+1 && u<w_pad-1 && v<w_pad-1
		gauss_im([u-rad:u+rad],[v-rad:v+rad],:) = test_pad([u-rad:u+rad],[v-rad:v+rad],:);
	else
		gauss_im(u,v,:) = test_pad(u,v,:);
	end

end

h = figure(4);
imshow(gauss_im);
set(h, 'Position', [win_size 0 win_size win_size]);




% Set up world
w_proj = 3;			% projection plane width
tric = 15;			% tri-mesh density
dis = -6;			% distance of screen from projector source point

plot_bool = 1;		% 0 for no ray plotting; 1 for ray plotting

% control points in grid form 
X = [-15 -15 -15 -15;
	  -5  -5  -5  -5;
	   5   5   5   5;
	  15  15  15  15];

Y = [0 5 5 0;
	 5 5 5 5;
	 5 5 5 5;
	 0 5 5 0];

Z = [ 15  5  -5 -15;
	  15  5  -5 -15;
	  15  5  -5 -15;
	  15  5  -5 -15 ];

% Evaluate and triangulate a patch
[Q,tri,x,y,z] = bpatch(X,Y,Z,tric);

h = figure(2);
set(h, 'Position', [1200 500 750 750]);
xlabel('x'); ylabel('y'); zlabel('z');
shading interp
grid;
axis vis3d
hold on;

% view(-32,-26)	% rear quarter
view(-35,15)	
% view(90,0)		% side view
% view(0,0)		% through projector
% view(-70,40)


proj_plane = [ w_proj/2  0  w_proj/2;
			   w_proj/2  0 -w_proj/2;
			  -w_proj/2  0  w_proj/2;
			  -w_proj/2  0 -w_proj/2;
			   0 dis 0 ];	% Origin here so that the transformation is 'wholesale'

proj_tri = [1 2 4;
			1 3 4];

% projector movements/transformations
proj_plane = rot_Ax_T(proj_plane,'x',-50);
proj_plane = trans_mat2(proj_plane,0,-9,-17);

o = proj_plane(5,:);

UL = proj_plane(3,:);
UR = proj_plane(1,:);
LR = proj_plane(2,:);
LL = proj_plane(4,:);

trimesh(proj_tri,proj_plane(:,1),proj_plane(:,2),proj_plane(:,3))
plot3(o(1),o(2),o(3),'go');
trimesh(tri,x,y,z);
text(o(1),o(2),o(3),'projector ray origin');


% Generate rays from the random samples
ray_plot = zeros(total_rays*2,3);
ray = zeros(total_rays,3);
data = zeros(total_rays,7);

for i = 1:total_rays
	u = r_samples(i,1)/w_pad;
	v = r_samples(i,2)/w_pad;

	rgb = reshape(test_pad(r_samples(i,2),r_samples(i,1),:),1,3);

	data(i,:) = [ double(rgb) u v 0 0 ];

	d = (1-u)*(1-v)*UL ...
		  + u*(1-v)*UR ...
		  + u*v*LR	 ...
		  + (1-u)*v*LL;

	ray_plot(i,:) = o;
    ray_plot(i+1,:) = d;

	d = d - o;
	ray(i,:) = d;
end

% % ray evaluation
f_param_ray = @(t,r,o) repmat(o,length(t),1) + [r(:,1).*t r(:,2).*t r(:,3).*t];

% Test for intersections
intsc = zeros(length(ray),3);

% parfor i = 1:length(ray)
for i = 1:length(ray)
	disp(sprintf('Tracing projection ray %d/%d (%.2f %%) \n',i,total_rays,100*i/total_rays))
	ray_buf = Inf;

	for j = 1:length(tri)
		% Construct points
		p1 = [x(tri(j,1)) y(tri(j,1)) z(tri(j,1))];
		p2 = [x(tri(j,2)) y(tri(j,2)) z(tri(j,2))];
		p3 = [x(tri(j,3)) y(tri(j,3)) z(tri(j,3))];

		% Intersection test
		[flag,u,v,t] = rayTriangleIntersection(o,ray(i,:),p1,p2,p3);

		if flag == 1					% if intersection exists given triangle j
			fl_uv_t = [flag,u,v,t];
			if t < ray_buf
				ray_buf = t;
			end

			k = (linspace(0,ray_buf,2))';			% terminate ray at intersection point
						 % since ray is straight, don't need too many eval points

			rplot = f_param_ray(k,ray(i,:),o);
			int_point = rplot(end,:);		% get the intersection point

			if plot_bool == 1
				
				
				% Plot ray
				plot3(rplot(:,1),rplot(:,2),rplot(:,3),'g');
				% Plot intersection point
				plot3(int_point(1),int_point(2),int_point(3),'*');

			end			% plot or not
			intsc(i,:) = int_point;
		end			% if
	end			% triangle loop
end			% ray loop






