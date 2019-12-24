% bezier2D.m
%% bezier2D: 2D prototype for image morph
function [Q,handle] = bezier2D(Cx,Cy,df,fig)
	dim = 2;

	N = [
		 -1  3 -3  1;
		  3 -6  3  0;
		 -3  3  0  0;
		  1  0  0  0
		 ];


	U = @(u) [u.^3 u.^2 u 1];
	W = @(w) [w.^3 w.^2 w 1]';


	f_bezier_patch = @(u,w) [U(u)*N*Cx*N*W(w) U(u)*N*Cy*N*W(w)];

	r = 0:df:1;
	s = 0:df:1;

	Q = randn(length(r),length(s),dim);


	for i = 1:length(r)
		for j = 1:length(s)
			P = f_bezier_patch(r(i),s(j));
			for k = 1:dim
				Q(i,j,k) = P(k);
			end
		end
	end


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
% end
