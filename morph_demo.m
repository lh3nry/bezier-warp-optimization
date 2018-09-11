% morph_demo.m
% Acknoledgment go to Francois Bouffard (for draggable.m) and Nathan Krislock 
% (for gui_mouse.m over which I have constructed my program); for without their efforts, 
% I would not have been able to finish such an ambitious goal.

function varargout = morph_demo(varargin)
	% CAD4 MATLAB code for CAD4.fig
	%      CAD4, by itself, creates a new CAD4 or raises the existing
	%      singleton*.
	%
	%      H = CAD4 returns the handle to a new CAD4 or the handle to
	%      the existing singleton*.
	%
	%      CAD4('CALLBACK',hObject,eventData,handles,...) calls the local
	%      function named CALLBACK in CAD4.M with the given input
	%      arguments.
	%
	%      CAD4('Property','Value',...) creates a new CAD4 or raises
	%      the existing singleton*.  Starting from the left, property value
	%      pairs are applied to the GUI before CAD4_OpeningFcn gets
	%      called.  An unrecognized property name or invalid value makes
	%      property application stop.  All inputs are passed to
	%      CAD4_OpeningFcn via varargin.
	%
	%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
	%      instance to run (singleton)".
	%
	% See also: GUIDE, GUIDATA, GUIHANDLES

	% Edit the above text to modify the response to help CAD4

	% Last Modified by GUIDE v2.5 22-Feb-2017 17:24:09

	% Begin initialization code - DO NOT EDIT
	gui_Singleton = 1;
	gui_State = struct('gui_Name',       mfilename, ...
					   'gui_Singleton',  gui_Singleton, ...
					   'gui_OpeningFcn', @CAD4_OpeningFcn, ...
					   'gui_OutputFcn',  @CAD4_OutputFcn, ...
					   'gui_LayoutFcn',  [] , ...
					   'gui_Callback',   []);
	if nargin && ischar(varargin{1})
		gui_State.gui_Callback = str2func(varargin{1});
	end

	if nargout
		[varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
	else
		gui_mainfcn(gui_State, varargin{:});
	end
	% End initialization code - DO NOT EDIT





% --- Executes just before CAD4 is made visible.
function CAD4_OpeningFcn(hObject, eventdata, handles, varargin)
	% This function has no output args, see OutputFcn.
	% hObject    handle to figure
	% eventdata  reserved - to be defined in a future version of MATLAB
	% handles    structure with handles and user data (see GUIDATA)
	% varargin   command line arguments to CAD4 (see VARARGIN)

	% close all

	% A=imread('test300.png');
	% A=imread('test600.png');
	A=imread('test.png');

	img_w = size(A,1);
	img_h = size(A,2);

	padding = 128;


	cla(handles.axes1);
	axis([-padding img_w+padding -padding img_h+padding]);
	% axis square;
	% img = imshow(A);

	% box on;
	hold on;

	vv = [];

	cp_grid = floor(linspace(0,img_w,4));

	[Cx, Cy] = meshgrid(cp_grid);

	Cx = reshape(Cx,16,1);
	Cy = reshape(Cy,16,1);

	for i = 1:16
		vv = [vv plot(Cx(i),Cy(i))];
	end

	% For visible vertices:
	vertexSize = 15;
	set(vv,'Marker','o','MarkerSize',vertexSize,'MarkerFaceColor','b');
	% For invisible vertices:
	%set(vv,'Marker','o','MarkerSize',10,'MarkerFaceColor','none', ...
	%       'MarkerEdgeColor','none');

	% Saving the vertex vector as application data
	% in the current axes (along with empty element p which will
	% later hold the handle to the polygon itself)
	setappdata(gca,'vv',vv);
	setappdata(gca,'img',[]);
	setappdata(gca,'isize',[img_w img_h]);
	setappdata(gca, 'A', A);
	% Cell Array to store the curves (as 4-points)

	% Calling draggable on each of the vertices, passing as an
	% argument the handle to the redraw_poly fucntion (see below)
	for i=1:length(vv)
		draggable(vv(i),@redraw_poly);
	end

	vv = reshape(vv,4,4);

	% Finally we draw the polygon itself using the redraw_poly
	% function, which can be found below
	redraw_poly;

	% Choose default command line output for CAD4
	handles.output = hObject;

	% Update handles structure
	guidata(hObject, handles);

	% UIWAIT makes CAD4 wait for user response (see UIRESUME)
	%uiwait(handles.fig_mouse);

% --- Outputs from this function are returned to the command line.
function varargout = CAD4_OutputFcn(hObject, eventdata, handles) 
	% varargout  cell array for returning output args (see VARARGOUT);
	% hObject    handle to figure
	% eventdata  reserved - to be defined in a future version of MATLAB
	% handles    structure with handles and user data (see GUIDATA)

	% Get default command line output from handles structure
	varargout{1} = hObject;


	% Update handles structure
	guidata(hObject, handles);

	

function redraw_poly(h)
	% Deleting previous drawn objects
	% delete(getappdata(gca,'im'));
	delete(getappdata(gca,'img'));

	% Retrieving the vertex vector and corresponding xdata and ydata

	vv = getappdata(gca,'vv');
	xdata = reshape(cell2mat(get(vv,'xdata'))',4,4);
	ydata = reshape(cell2mat(get(vv,'ydata'))',4,4);


	isize = getappdata(gca,'isize');
	img_w = isize(1);
	img_h = isize(2);

	[Q,hand] = bezier2D_pix(xdata,ydata,img_w,0);

	lsp = linspace(0,img_w,img_w);
	uni = reshape([repmat(lsp,img_w,1) repmat(lsp,img_w,1)'],img_w,img_w,2);

	DxDy = round(uni-Q);

	A = getappdata(gca,'A');
	% 2015b (?) or after
	% I2 = imwarp(A,DxDy,'FillValues',[0;255;0],'Interp','linear'); 
	% Local copy of 2016b imwarp
	I2 = imwarp_local(A,DxDy,'FillValues',[0;255;0],'Interp','linear');

	img = imshow(I2);				% plot image
	setappdata(gca,'img',img);
    
	% Reshuffling the render order so the control points are accessible/visible
	% uistack(im,'bottom');
	uistack(img,'bottom');

% --- Executes on slider movement.
% function slider3_Callback(hObject, eventdata, handles)
% 	% hObject    handle to slider3 (see GCBO)
% 	% eventdata  reserved - to be defined in a future version of MATLAB
% 	% handles    structure with handles and user data (see GUIDATA)

% 	% Hints: get(hObject,'Value') returns position of slider
% 	%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
% 	vertexSize = 7*get(handles.slider3,'Value') + 10
% 	vv = getappdata(gca,'vv');
% 	set(vv,'Marker','o','MarkerSize',vertexSize);
% 	redraw_poly;

% % --- Executes during object creation, after setting all properties.
% function slider3_CreateFcn(hObject, eventdata, handles)
% 	% hObject    handle to slider3 (see GCBO)
% 	% eventdata  reserved - to be defined in a future version of MATLAB
% 	% handles    empty - handles not created until after all CreateFcns called

% 	% Hint: slider controls usually have a light gray background.
% 	if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
% 		set(hObject,'BackgroundColor',[.9 .9 .9]);
% 	end


% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    I2 = getappdata(gca,'img');
    imwrite(I2.CData,'output.png');
    