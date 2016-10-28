% minimal working example of overlaying multiple/different colormaps
% ktr oct 28, 2016

% This problem occurs time and again, where it might be useful to use
%   multiple colormaps or plots on the same axes in matlab. Here is an
%   example of how to do that. 
% This example plots a grid of points, then defines a given region of 
%   interest (ROI) that we want to map in a different colormap. This can be 
%   applied to other plotting projects as well 
%%
% some big grid of values
z = log10(rand(100,100)/25);
    x = 1:1:length(z);
    y = 1:1:length(z);
% your ROI region and values
z1 = log10(rand(50,50));
    x1 = 25:1:75;
    y1 = 25:1:75;
% if you want to keep dynamic range same, define it up front:
dynRange = [-2.5 0];

% PLOT ------------------------------
figure,
   % first axes
    ax1 = axes;
    imagesc(x,y,z,dynRange)
    % label axes and definitions before defining ax2
    hx = xlabel('x'); hy = ylabel('y');
    ht = title('Two colormaps!');
    set(gca, 'FontSize',18)
   % second axes
    view(2)
    ax2 = axes;
    imagesc(x1,y1,z1,dynRange)
    % Link axes
    linkaxes([ax1,ax2])
    % Hide top axes
    ax2.Visible = 'off';
    ax2.XTick = [];
    ax2.YTick = [];
    % Give each axes its own colormap
    colormap(ax1,'gray')
    colormap(ax2,'hot')
    hold on, 
    
    % plot your roi boundaries too (something like this...)
    dx1 = abs(x1(2)- x1(1));
    dy1 = abs(y1(2)- y1(1));
    xbox = [x1(1)-dx1 x1 x1(end)+dx1];
    ybox = [y1(1)-dy1 y1 y1(end)+dy1];
    % horizontal lines
    hlineroi(1,:) = line(xbox, repmat(ybox(1),   1,length(x1)+2));
    hlineroi(2,:) = line(xbox, repmat(ybox(end),1,length(x1)+2));
    % vertical lines
    hlineroi(3,:) = line(repmat(xbox(1),  1,length(y1)+2) ,ybox);
    hlineroi(4,:) = line(repmat(xbox(end),1,length(y1)+2) ,ybox);
    set(hlineroi, 'LineStyle','-', 'LineWidth', 5, 'Color', 'm')
    
