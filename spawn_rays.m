% spawn_rays.m
%% spawn_rays: uniformly samples the projector image plane and generates rays
function [rays, plotting] = spawn_rays(r_width, r_height, proj, proj_origin)
	rays = zeros(r_height*r_width,3);
	plotting = zeros(r_height*r_width*2,3);

	count = 1;
	for i = linspace(0,1,r_width)
		for j = linspace(0,1,r_height)
			rays(count,:) = bilinear_interp(proj,j,i);
			plotting(count,:) = rays(count,:);
			plotting(count + 1,:) = proj_origin;
			count = count + 2;
		end
	end
