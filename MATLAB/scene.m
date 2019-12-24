%% Setup simulation scene

%% Setup view plane; where the image is generated using the intersected rays
w = 7;				% view plane width
dis = -7;			% distance of image capture plane from viewpoint

view_plane = [ w/2  0  w/2;
			   w/2  0 -w/2;
			  -w/2  0  w/2;
			  -w/2  0 -w/2;
			   0 dis 0 ];	% Origin here so that the transformation is 'wholesale'

view_tri = [1 2 4;
			1 3 4];

view_plane = trans_mat2(view_plane,0,-25,0);
viewpoint = view_plane(5,:);

UL = view_plane(3,:);
UR = view_plane(1,:);
LR = view_plane(2,:);
LL = view_plane(4,:);

trimesh(view_tri,view_plane(:,1),view_plane(:,2),view_plane(:,3));
plot3(viewpoint(1),viewpoint(2),viewpoint(3),'ro');
text(viewpoint(1),viewpoint(2),viewpoint(3),'viewpoint');

%% Setup the projection plane that simulates projector output
w_proj = 3;			% projection plane width
dis = -6;			% distance of screen from projector source point

proj_plane = [ w_proj/2  0  w_proj/2;
			   w_proj/2  0 -w_proj/2;
			  -w_proj/2  0  w_proj/2;
			  -w_proj/2  0 -w_proj/2;
			   0 dis 0 ];	% Origin here so that the transformation is 'wholesale'

proj_tri = [1 2 4;
			1 3 4];

proj_plane = rot_Ax_T(proj_plane,'x',-50);
proj_plane = trans_mat2(proj_plane,0,-9,-17);

o = proj_plane(5,:); % origin of the projector

trimesh(proj_tri,proj_plane(:,1),proj_plane(:,2),proj_plane(:,3))
plot3(o(1),o(2),o(3),'go');
text(o(1),o(2),o(3),'projector ray origin');


%% Generate Bezier patch to simulate projection surface
patchdensity = 15;			% patch tri-mesh density

% control points of the patch in grid form 
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

[Q,tri,x,y,z] = bpatch(X,Y,Z,patchdensity);
% trimesh(tri,x,y,z);
% surf(x,y,z);
surf(Q(:,:,1),Q(:,:,2),Q(:,:,3))
shading interp
