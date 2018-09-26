% new_run.m


close all;
clear all;

preview_cam

scene

im = imread('colour_test.png');

% figure(2);
% imshow(im);


P = proj_plane(1:4,:);

[rays, plt] = spawn_rays(10,10,P,o);


figure(1);
hold on;

plot3(plt(:,1),plt(:,2),plt(:,3),'g');
plot3(P(:,1),P(:,2),P(:,3),'b*');

bvh = [max([x y z]) ; min([x y z])]



N = [
	 -1  3 -3  1;
	  3 -6  3  0;
	 -3  3  0  0;
	  1  0  0  0
	 ];

Ax = N * X * N';
Ay = N * Y * N';
Az = N * Z * N';
d = rays(1,:);
o = rays(2,:);
tol = 1e-3;

U = @(u) [u.^3 u.^2 u.^1 u.^0];
Udu = @(u) [3.*u.^2 2.*u ones(size(u)) zeros(size(u))];

J = @(u,v,t) [ Udu(u) * Ax * U(v)' U(u) * Ax * Udu(v)' d(1) ; ...
			   Udu(u) * Ay * U(v)' U(u) * Ay * Udu(v)' d(2) ; ...
			   Udu(u) * Az * U(v)' U(u) * Az * Udu(v)' d(3) ];

eval_bezier = @(u,w) [U(u)*Ax*U(w)'; U(u)*Ay*U(w)'; U(u)*Az*U(w)'];
F = @(u,v,t) [ eval_bezier(u,v) - o' - t.*d' ] ;

F(0,0,0)
J(0,0,0)

J(0,0,0)\F(0,0,0)