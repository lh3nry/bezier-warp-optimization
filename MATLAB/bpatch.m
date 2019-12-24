% bpatch.m
%% bpatch: Gives a Bezier patch with triangulation
function [Q,tri,x,y,z] = bpatch(Cx,Cy,Cz,n)
	N = [
		 -1  3 -3  1;
		  3 -6  3  0;
		 -3  3  0  0;
		  1  0  0  0
		 ];
	U = @(u) [u.^3 u.^2 u u.^0];
	W = @(w) [w.^3 w.^2 w w.^0]';

	f_bezier_patch = @(u,w) [U(u)*N*Cx*N*W(w) U(u)*N*Cy*N*W(w) U(u)*N*Cz*N*W(w)];

	r = linspace(0,1,n);
	s = r;

	B = f_bezier_patch(r',s');
	Q = reshape(B,length(r),length(s),3);

	% Convert tensor into list of 3D points
	Qxyz = reshape(Q,length(r)^2,3);
	x = Qxyz(:,1);
	y = Qxyz(:,2);
	z = Qxyz(:,3);

	% triangulate
	tri = [];
	n2 = length(r)^2;
	for i = 1:(n2-(n+1))
		if mod(i,n) ~= 0
			tri = [tri; i i+1 i+n];
			tri = [tri; i+1 i+n+1 i+n];
		end
	end
