% rayQuad.m
%% rayQuad: Intersection of quadrilaterals with rays
function [flag,u,v,t] = rayQuad(o,d,v00,v10,v11,v01)
	EPS = 1e-5;

	e01 = v10 - v00;
	e03 = v01 - v00;

	P = cross(d,e03);
	DET = dot(e01,P);
	if abs(DET) < EPS
		[flag,u,v,t] = deal(0,0,0,0);
	end
	T = o - v00;
	ALPHA = dot(T,P)/DET;

	if ALPHA < 0
		[flag,u,v,t] = deal(0,0,0,0);
	end
	% if ALPHA > 1
	% 	[flag,u,v,t] = deal(0,0,0,0);
	% end

	Q = cross(T,e01);
	BETA = dot(d,Q)/DET;

	if BETA < 0
		[flag,u,v,t] = deal(0,0,0,0);
	end
	% if BETA > 1
	% 	[flag,u,v,t] = deal(0,0,0,0);
	% end

	if (ALPHA + BETA) > 1
		e23 = v01 - v11;
		e21 = v10 - v11;
		P_ = cross(d,e21);
		DET_ = dot(e23,P_);
		if abs(DET_) < EPS
			[flag,u,v,t] = deal(0,0,0,0);
		end
		T_ = o - v11;
		ALPHA_ = dot(T_,P_)/DET_;
		if ALPHA_ < 0
			[flag,u,v,t] = deal(0,0,0,0);
		end
		Q_ = cross(T_,e23);
		BETA_ = dot(d,Q_)/DET_;
		if BETA_ < 0
			[flag,u,v,t] = deal(0,0,0,0);
		end
	end

	t = dot(e03,Q)/DET;
	if t < 0
		[flag,u,v,t] = deal(0,0,0,0);
	end


	e02 = v11 - v00;
	N = cross(e01,e03);

	if (abs(N(1)) >= abs(N(2))) & (abs(N(1)) >= abs(N(3)))
		ALPHA11 = (e02(2)*e03(3) - e02(2)*e03(3))/N(1);
		BETA11 =  (e01(2)*e02(3) - e01(1)*e02(2))/N(1);
    elseif (abs(N(2)) >= abs(N(1))) & (abs(N(2)) >= abs(N(3)))
        ALPHA11 = (e02(3)*e03(1) - e02(1)*e03(3))/N(2);
		BETA11 =  (e01(3)*e02(1) - e01(1)*e02(3))/N(2);
	else
		ALPHA11 = (e02(1)*e03(2) - e02(2)*e03(1))/N(3);
		BETA11 =  (e01(1)*e02(2) - e01(2)*e02(1))/N(3);
    end

    if abs(ALPHA11 - 1) < EPS
    	u = ALPHA;
    	if abs(BETA11 - 1) < EPS
    		v = BETA;
    	else
    		v = BETA/(u*(BETA11 - 1) + 1);
    	end
    elseif abs(BETA11 - 1) < EPS
    	v = BETA;
    	u = ALPHA/(v*(ALPHA11 - 1) + 1);
	else
		A = -(BETA11 - 1);
		B = ALPHA*(BETA11 - 1) - BETA*(ALPHA11 - 1) - 1;
		C = ALPHA;
		DELTA = B^2 - 4*A*C;
		Q = -0.5*(B + sign(B)*sqrt(DELTA));
		u = Q/A;
		if (u < 0) || (u > 1)
			u = C/Q;
		end
		v = BETA/(u*(BETA11 - 1) + 1);
	end


	[flag,u,v,t] = deal(1,u,v,t);

