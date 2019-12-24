% plot_quad.m
%% plot_quad: draws a quad defined by 4 vertices
% v0----------v1
% |           |
% |           |
% |           |
% |           |
% v2----------v3
% 


function h = plot_quad(fig,v0,v1,v2,v3,linesty)
	figure(fig)
	hold on;
	% v0-v1
	plot3([v0(1);v1(1)],[v0(2);v1(2)],[v0(3);v1(3)],linesty);
	% v0-v2
	plot3([v0(1);v2(1)],[v0(2);v2(2)],[v0(3);v2(3)],linesty);
	% v1-v3
	plot3([v3(1);v1(1)],[v3(2);v1(2)],[v3(3);v1(3)],linesty);
	% v2-v3
	plot3([v3(1);v2(1)],[v3(2);v2(2)],[v3(3);v2(3)],linesty);
