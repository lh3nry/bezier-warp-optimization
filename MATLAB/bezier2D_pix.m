% bezier2D_pix.m
%% bezier2D_pix: 2D prototype for image morph
function [Q,handle] = bezier2D_pix(Cx,Cy,pix,fig)
	dim = 2;

	r = linspace(0,1,pix);
	s = linspace(0,1,pix);

	N = [
		 -1  3 -3  1;
		  3 -6  3  0;
		 -3  3  0  0;
		  1  0  0  0
		 ];

	U = @(u) [u.^3 u.^2 u u.^0];
	W = @(w) [w.^3 w.^2 w w.^0]';

	f_bezier_patch = @(u,w) [U(u)*N*Cx*N*W(w) U(u)*N*Cy*N*W(w)];

	B = f_bezier_patch(r',s');

	Q = reshape(B,length(r),length(s),2);

	if fig > 0
		h = figure(fig);
		% axis square;
		% axis([-padding w+padding -padding w+padding]);
		hold on;
		handle = surface(Q(:,:,1),Q(:,:,dim),zeros(length(r),length(s)));
		% shading interp
		grid;

		axis square
		axis equal
		view(0,90);

		plot(Cx,Cy,'ro');
	% elseif condition
	% 	body
	else
		handle = 0;
	end

	

% end
