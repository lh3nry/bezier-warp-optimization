% new_run.m


close all;
clear all;

preview_cam

scene

im = imread('colour_test.png');

figure(2);
imshow(im);



% r_height = 10;
% r_width = r_height;

% [X,Y] = meshgrid(linspace(1,size(im,1),r_height),linspace(1,size(im,2),r_width));

% rays = zeros(r_height*r_width,6);

P = proj_plane(1:4,:);


% for i = 1:r_height
% 	for j = 1:r_width
% 		% size(rays(i*r_width + j, :))
% 		% size(projector_ray(o,P,X(j),Y(i),im))
% 		rays(i*r_width + j, :) = projector_ray(o,P,X(j),Y(i),im);
% 	end
% end

rays = zeros(7,6);
rays(1,:) = projector_ray(o,P,1,1,im)
rays(2,:) = [o 0 0 0]
rays(3,:) = projector_ray(o,P,1,1024,im)
rays(4,:) = [o 0 0 0]
rays(5,:) = projector_ray(o,P,1024,1,im)
rays(6,:) = [o 0 0 0]
rays(7,:) = projector_ray(o,P,1024,1024,im)


figure(1);
hold on;
% os = repmat(o,size(rays,1),1);
% quiver3(os(:,1),os(:,2),os(:,3), rays(:,1),rays(:,2),rays(:,3));
plot3(rays(:,1),rays(:,2),rays(:,3),'g');
plot3(rays([1 3 5 7],1),rays([1 3 5 7],2),rays([1 3 5 7],3),'r*');

