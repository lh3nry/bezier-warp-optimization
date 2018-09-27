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

U = @(u) [u.^3 u.^2 u.^1 u.^0];
Udu = @(u) [3.*u.^2 2.*u ones(size(u)) zeros(size(u))];



eval_bezier = @(u,w) [U(u)*Ax*U(w)'; U(u)*Ay*U(w)'; U(u)*Az*U(w)'];

% proj_plane = rot_Ax_T(proj_plane,'x',-50);
% proj_plane = trans_mat2(proj_plane,0,-9,-17);
% xx = [0 0 0];
% Feval = F_(xx);
% Jeval = J_(xx);
% o = rays(2,:);
% invv = J(0,0,0)\F(0,0,0)
tol = 1e-7;  it_max = 10; t_max = 15; 
% o = [0 0 0];
for I = 1:length(rays)
	xx = [0 0 0]; it_count = 0;
	d = rays(I,:) - o;
	% d = d/norm(d);
	% plot3([d(1) - o(1)],[d(2) - o(2)],[d(3) - o(3)],'r*')
	plot3([d(1)],[d(2)],[d(3)],'r*')
	J = @(u,v,t) [ Udu(u) * Ax * U(v)' U(u) * Ax * Udu(v)' -d(1) ; ...
				   Udu(u) * Ay * U(v)' U(u) * Ay * Udu(v)' -d(2) ; ...
				   Udu(u) * Az * U(v)' U(u) * Az * Udu(v)' -d(3) ];
	J_ = @(x) J(x(1),x(2),x(3));

	F = @(u,v,t) [ eval_bezier(u,v) - o' - t.*d' ] ;
	F_ = @(x) F(x(1),x(2),x(3));

	newt_update = repmat(tol + 1,3,1);

	while abs(xx(3)) < t_max && (newt_update(1) >= tol || newt_update(2) >= tol) && it_count <= it_max
	% while it_count <= it_max
		fprintf(1, 'iteration: %d. u,v,t = %.4f, %.4f, %.2f \n', it_count, xx(1), xx(2), xx(3));
		newt_update = -J_(xx)\F_(xx);
		xx = xx + newt_update';
		it_count = it_count + 1;
	end

	% o = proj_plane(5,:); % origin of the projector

	rt_point = eval_bezier(xx(1),xx(2))'
	% line(o,rt_point,'Color','r','LineWidth',1,'LineStyle','-')
	plot3([rt_point(1) o(1)],[rt_point(2) o(2)],[rt_point(3) o(3)],'b-')
end





