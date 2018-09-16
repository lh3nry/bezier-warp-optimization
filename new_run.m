% new_run.m


close all;
clear all;

preview_cam

scene

im = imread('colour_test.png');

figure(2);
imshow(im);



r_height = 10;
r_width = r_height;

P = proj_plane(1:4,:);

rays = zeros(8,3);
rays(1,:) = projector_ray(o,P,0,0,im);
rays(3,:) = projector_ray(o,P,0,1,im);
rays(5,:) = projector_ray(o,P,1,0,im);
rays(7,:) = projector_ray(o,P,1,1,im);

rays(2,:) = o;
rays(4,:) = o;
rays(6,:) = o;
rays(8,:) = o;

figure(1);
hold on;

plot3(rays(:,1),rays(:,2),rays(:,3),'g');
plot3(rays([1 3 5 7],1),rays([1 3 5 7],2),rays([1 3 5 7],3),'r*');
plot3(P(:,1),P(:,2),P(:,3),'b*');

