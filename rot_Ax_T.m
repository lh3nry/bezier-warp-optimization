% rot_Ax_T.m
%% rot_Ax_T: Given Axis and Theta, rotates a matrix of points Nx3
function [P_] = rot_Ax_T(P,Ax,theta)
	theta = deg2rad(theta);
	if Ax == 'x'
		rot = [1 0 0; 
		0 cos(theta) -sin(theta); 
		0 sin(theta) cos(theta)];
	elseif Ax == 'y'
		rot = [cos(theta) 0 sin(theta);
			   0 1 0;
			   -sin(theta) 0 cos(theta)];
	elseif Ax == 'z'
		rot = [cos(theta) -sin(theta) 0;
				sin(theta) cos(theta) 0; 
				0 0 1];
	else
		rot = eye(3);
	end

	P_ = P*rot;
