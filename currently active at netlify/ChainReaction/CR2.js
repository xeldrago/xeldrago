	//grid_sz, cell_sz, img_sz, total_users 
	//must be initialised before-hand
	var grid_sz;//=10;
	//var box_sz=15;
	var cell_sz;//=75;
	var img_sz;//=50;
	var total_users;
	var tmp_cur_uid;
	var is_first_move=1;
	var grid ;
	var tmp_grid;
	
	var prev_grid;//to enable 'undo' feature
	var prev_user=1;//to store the prev user's turn

	var cur_Uid=1;
	var angleArray;
	var alive_users;
	var move_count;
	var is_my_move=0;
	var color_Array = ['#FF0000','#00FF00','#0000FF','#FFFF00','#00FFFF','#AABBCC','#0A0B0C','#C8B9AA','#671234','#ABCD01'];
	//var color_count=0;
	//var isTurn=0;
	var animateArray;
	var animateCount = 0;
	var animateInterval;
	var animateIterations = 0;
	var animateRadius = 10;
	var isMouseEnabled=0;
	var userName;
	var userId;
	var angle = 0.0;
	var ctx;
	//called once at the start
	//mainly used to create all the dynamic arrays
	function createArrays(){
		grid = new Array(grid_sz);
		prev_grid = new Array(grid_sz);
		tmp_grid = new Array(grid_sz);
		angleArray = new Array(grid_sz);
		animateArray = new Array(grid_sz*grid_sz);
		alive_users = new Array(total_users+1);

		move_count = 0;

		for(i=0; i<=total_users; i++)
			alive_users[i] = 1;

		for(i=0; i<grid_sz; ++i)
		{
			angleArray[i] = new Array(grid_sz);
			grid[i] = new Array(grid_sz);
			tmp_grid[i] = new Array(grid_sz);
			prev_grid[i] = new Array(grid_sz);
		}
		for(i=0; i<grid_sz*grid_sz; ++i)
		{
			animateArray[i] = new Array(2);
		}
		for(i=0;i<grid_sz;++i)
		{
			for(j=0;j<grid_sz;++j)
			{
				grid[i][j]=0;
				angleArray[i][j]=Math.floor(Math.random()*360);
			}
		}
		isMouseEnabled = 1;
	}

	//******************'pure' helper functions for animating*********
	function getpos(event)
    {
      var x = new Number();
      var y = new Number();
      var canvas = document.getElementById("myCanvas");

      if (event.x !== undefined && event.y !== undefined)
      {
        x = event.x;
        y = event.y;
      }
      

      x -= canvas.offsetLeft;
      y -= canvas.offsetTop;
      y += document.body.scrollTop;
      update(Math.floor(x/cell_sz),Math.floor(y/cell_sz));
    }
    function isCorners(x,y)
    {
		return (x===0 && y==grid_sz-1 || x==grid_sz-1 && y==grid_sz-1 || x===0 && y===0 || x==grid_sz-1 && y===0 );
    }
    function isOnEdge(x,y)
    {
		return (x==0 || y==0 || x==grid_sz-1 || y==grid_sz-1);
    }
    function isInside(x,y)
    {
		return !isCorners(x,y) && !isOnEdge(x,y);
    }
    function isExpandable(c,x,y)
    {
		return (c==1 && isCorners(x,y) ||
				c==2 && isOnEdge(x,y) ||
				c==3 && isInside(x,y));
    }
    //****************End of Helper functions*********************


    //		calling sequence:
    //				-->createAnimation() --> rebuild() --> animate() -->
    //              |__________________________________________________|
    //
    //		
    function animate()
    {
		var white = "#ffffff";
		for(var i=0; i<animateCount; ++i)
		{
			var tx=animateArray[i][0],ty=animateArray[i][1];
			var curCol = color_Array[Math.floor(grid[tx][ty]/10)];
			
			if(tx>0)//draw to left of it...
			{
				if(animateIterations>0)
				{
					ctx.fillStyle=white;
					ctx.beginPath();
					ctx.arc(tx*cell_sz + hlf - animateIterations+1,
					ty*cell_sz +hlf ,
					animateRadius,
					0,2*Math.PI);
					ctx.fill();
				}

				ctx.fillStyle = curCol;
				ctx.beginPath();
				var hlf=cell_sz/2.0;
				ctx.arc(tx*cell_sz + hlf - animateIterations,
					ty*cell_sz +hlf ,
					animateRadius,
					0,2*Math.PI);
				ctx.fill();
				
				
			}

			if(tx<grid_sz-1)//draw towards the right...
			{
				if(animateIterations>0)
				{
					ctx.fillStyle=white;
					ctx.beginPath();
					var hlf=cell_sz/2.0;
					ctx.arc(tx*cell_sz + hlf + animateIterations-1,
						ty*cell_sz +hlf ,
						animateRadius,
						0,2*Math.PI);
				ctx.fill();
				}
				ctx.fillStyle = curCol;
				ctx.beginPath();
				var hlf=cell_sz/2.0;
				ctx.arc(tx*cell_sz + hlf + animateIterations,
					ty*cell_sz +hlf ,
					animateRadius,
					0,2*Math.PI);
				ctx.fill();
			}

			if(ty>0)//draw on top...
			{
				if(animateIterations>0)
				{
					ctx.fillStyle=white;
					ctx.beginPath();
					var hlf=cell_sz/2.0;
					ctx.arc(tx*cell_sz + hlf,
						ty*cell_sz +hlf - animateIterations+1,
						animateRadius,
						0,2*Math.PI);
					ctx.fill();
				}
				ctx.fillStyle = curCol;
				ctx.beginPath();
				var hlf=cell_sz/2.0;
				ctx.arc(tx*cell_sz + hlf,
					ty*cell_sz +hlf - animateIterations,
					animateRadius,
					0,2*Math.PI);
				ctx.fill();
			}

			if(ty<grid_sz-1)//draw on bottom..
			{
				if(animateIterations>0)
				{
					ctx.fillStyle=white;
					ctx.beginPath();
					var hlf=cell_sz/2.0;
					ctx.arc(tx*cell_sz + hlf,
						ty*cell_sz +hlf + animateIterations-1,
						animateRadius,
						0,2*Math.PI);
					ctx.fill();
			}
				ctx.fillStyle = curCol;
				ctx.beginPath();
				var hlf=cell_sz/2.0;
				ctx.arc(tx*cell_sz + hlf,
					ty*cell_sz +hlf + animateIterations,
					animateRadius,
					0,2*Math.PI);
				ctx.fill();
			}
		
		}

		animateIterations++;
		if(animateIterations>75)
		{
			ctx.fillStyle="rgb(200,200,200)";
			var tmp = document.getElementById("myCanvas");
			for(i=0; i<=grid_sz; ++i)
			{
				//for(var j=0; j<50; ++j)
					ctx.fillRect(i*cell_sz, 0, 1, tmp.height);
					ctx.fillRect( 0, i*cell_sz, tmp.width, 1);
			}
			clearInterval(animateInterval);
			rebuild();
		}
		
	}
	function rebuild()
	{
		for(var i=0;i<animateCount;++i)
		{
			if(animateArray[i][0]>0)
				tmp_grid[animateArray[i][0]-1][animateArray[i][1]]++;
			if(animateArray[i][0]<grid_sz-1)
				tmp_grid[animateArray[i][0]+1][animateArray[i][1]]++;
			if(animateArray[i][1]>0)
				tmp_grid[animateArray[i][0]][animateArray[i][1]-1]++;
			if(animateArray[i][1]<grid_sz-1)
				tmp_grid[animateArray[i][0]][animateArray[i][1]+1]++;
		}
		createAnimation();
    }
    function createAnimation()
    {
		animateCount=0;
		//alert("hi");
		
	//	animateArray[animateCount][0] = x;
	//	animateArray[animateCount][1] = y;
	//	animateCount++;
		for(var i=0;i<grid_sz;++i)
		{
			for(var j=0;j<grid_sz;++j)
			{
				var cur_cnt = grid[i][j]%10 + tmp_grid[i][j];
				if(cur_cnt>1 && isCorners(i,j) ||
					cur_cnt>2 && isOnEdge(i,j) ||
					cur_cnt>3&& isInside(i,j))
				{
					animateArray[animateCount][0] = i;
					animateArray[animateCount][1] = j;
					animateCount++;
					var prev =grid[i][j];
					var upd_val;
					if(isCorners(i,j))
					upd_val = cur_cnt-2;
					else if(isOnEdge(i,j))
					upd_val = cur_cnt-3;
					else if(isInside(i,j))
					upd_val = cur_cnt-4;/*
					if(prev%10==0)
					{
						//alert(i+" "+j + "<-"+prev+cur_cnt);
						grid[i][j] = 10*cur_Uid + cur_cnt;
						if(isCorners(i,j)) grid[i][j] -= 2;
						else if(isOnEdge(i,j)) grid[i][j] -= 3;
						else if(isInside(i,j)) grid[i][j] -= 4
					//	alert(grid[i][j]+" "+i+" "+j + "<-"+prev+cur_cnt);
					}*/

						grid[i][j] = 10*cur_Uid + upd_val;

				//	alert("hi"+grid[i][j]+" "+i+","+j);
				}
				else if(tmp_grid[i][j]>0)
				{
						grid[i][j] = cur_Uid*10 + cur_cnt;
				//	alert("set:"+i+","+j+"->"+grid[i][j]+" in ");
				}
				tmp_grid[i][j]=0;

			}
		}
		animateIterations=0;
		if(animateCount>0)
			animateInterval = setInterval(animate, 1);
		else
		{
			//isAnimating=0;
			//alert("is reset!");
			check_fin();
			ready_for_next();
			return;
		}
	}

	function is_alive(id)
	{
		for(i=0; i<grid_sz;i++)
		{
			for(j=0;j<grid_sz;j++)
			{
				if(grid[i][j]%10 > 0 && Math.floor(grid[i][j]/10) == id)
					return true;
			}
		}
		return false;
	}
	
	/*	mouse-down -> getpos() -> update() */
	function update(x,y)
    {
		var tmp = grid[x][y];
		if(isMouseEnabled==0)
			return;
		//alert(tmp);
  //	check if it is a valid move..
		
//		alert(Math.floor(tmp/10) + " "+ cur_Uid);
		if(tmp%10>0 && Math.floor(tmp/10) != cur_Uid)
			return;
		//alert("here");
//		cur_Uid = (cur_Uid)%2 + 1;
		
	//	isAnimating=1;
		isMouseEnabled = 0;

		//first copy the current board inorder to 'revert'
		for(i=0;i<grid_sz;i++)
		{
			for(j=0;j<grid_sz;j++)
				prev_grid[i][j] = grid[i][j];
		}
		prev_user = cur_Uid;
		document.getElementById('ud').style.display = "none";
		if(tmp%10===0)
		{//new cell to be put here...
		//	alert("Got!");
			grid[x][y] = cur_Uid*10 + 1;
			angleArray[x][y]=0;
			ready_for_next();
		//	isAnimating=0;
			/*draw_Ball((grid[x][y]%10).toString(),
						cell_sz*x + Math.floor(cell_sz/2), 
						cell_sz*y + Math.floor(cell_sz/2),
						img_sz
						,angleArray[x][y],
						"#00f0ff");*/
		//	alert(grid[x][y]);
		}
		else if(!isExpandable(tmp%10,x,y))
		{//simply put on new image..
			grid[x][y] = cur_Uid*10 + (tmp%10)+1;
			ready_for_next();
	//		isAnimating=0;
			//alert(grid[x][y]);
			/*draw_Ball((grid[x][y]%10).toString(),
						cell_sz*x + Math.floor(cell_sz/2), 
						cell_sz*y + Math.floor(cell_sz/2),
						img_sz
						,angleArray[x][y],
						"#00f0ff");*/
		//	alert("nothign!!");
		}
		else
		{//animate it to expand...
		//	alert("nothign!!");

			for(var i=0;i<grid_sz;++i)
			{
				for(var j=0;j<grid_sz;++j)
					tmp_grid[i][j]=0;
			}
			tmp_grid[x][y]=1;
		/*	if(x>0) tmp_grid[x-1][y]++;
			if(x<grid_sz-1) tmp_grid[x+1][y]++;
			if(y>0) tmp_grid[x][y-1]++;
			if(y<grid_sz-1) tmp_grid[x][y+1]++;
		*/	//var unstble = 1;
			createAnimation();
		}
    }
	function undo()
	{
		for(i=0;i<grid_sz;i++)
		{
			for(j=0;j<grid_sz;j++)
				grid[i][j] = prev_grid[i][j];
		}
		cur_Uid = prev_user;
		paint_Lines(color_Array[cur_Uid]);
    }
    //sets all the variables for the next move
	function ready_for_next()
	{
		move_count++;

		tmp2 = cur_Uid%total_users + 1;
		

		while( !is_alive(tmp2) && move_count>total_users && tmp2!=cur_Uid)
			tmp2 = tmp2%total_users + 1;

		console.log(grid);
		//console.log('Id'+)
		if(tmp2==cur_Uid)//if this is equal, then game over
			alert("Game over");
		cur_Uid = tmp2;
		if(cur_Uid ==0)
			cur_Uid = 1;
		paint_Lines(color_Array[cur_Uid]);
		isMouseEnabled = 1;
		document.getElementById('ud').style.display = "block";
		//check_fin();
	}
    function check_fin()
    {
		var left_cnt=0;
		var gotfirst = 0;
		var first_uid;// = Math.floor(grid[0][0]/10);

		for(var i=0; i<grid_sz;++i)
		{
			for(var j=0; j<grid_sz; ++j)
			{
				if(grid[i][j]>0)
				{
					if(gotfirst==0)
					{
						first_uid = Math.floor(grid[i][j]/10);
						gotfirst=1;
					}
					else if(first_uid!=Math.floor(grid[i][j]/10))
						return false;
				}
			}
		}
		//alert("Your game is finished!");
		//reset the game...
		//clearInterval(animateInterval);
		resetGame();
		return true;
    }
	function resetGame()
	{
		for(var i=0; i<grid_sz;++i)
		{
			for(var j=0; j<grid_sz; ++j)
			{
				grid[i][j]=0;
			}
		}
	}
    //function that updates the actual board
    //for changing values
    //runs continuously in the game
    function startt() {
		for(var i=0; i<grid_sz;++i)
		{
			for(var j=0; j<grid_sz;++j)
			{
				if(grid[i][j]>0 && grid[i][j]%10 > 0)
				{
					var tmpAngle ;
					if(!isCorners(i,j) &&  ((isOnEdge(i,j)&&Math.floor(grid[i][j]%10)<=1)||
							(isInside(i,j)&&Math.floor(grid[i][j]%10)<3))
							)
						tmpAngle = 0;
					else
					{

						tmpAngle = angleArray[i][j];
						angleArray[i][j] = (angleArray[i][j]+10)%360;
					}
					draw_Ball((grid[i][j]%10).toString(),
						cell_sz*i + Math.floor(cell_sz/2),
						cell_sz*j + Math.floor(cell_sz/2),
						img_sz,
						tmpAngle,
						color_Array[Math.floor(grid[i][j]/10)]);
						
				}
				else
				{
					ctx.fillStyle = "#ffffff";
					ctx.fillRect(i*cell_sz+1,j*cell_sz+1,cell_sz-2,cell_sz-2);
				}
			}
		}
	//	draw_Ball("3",37,37,50,angle,"#ff0000");
	//	angle = (angle+10)%360;
	}
	function draw_Ball(img,x,y,sz,ang,col)
	{
		//x,y=> center of the image..
	//	alert(img+" jjjj" );
		ang = (Math.PI*(ang))/90.0;
		ctx.translate(x,y);
		ctx.fillStyle="#ffffff";
		ctx.beginPath();
		var hlf=sz/2.0;
		ctx.arc(0,0,(hlf)*Math.sqrt(2),0,2*Math.PI);
		ctx.fill();
		ctx.rotate(ang);
		ctx.fillStyle=col;
		ctx.fillRect(-hlf,-hlf,sz,sz);
		try{
		ctx.drawImage(document.getElementById(img), -hlf, -hlf,sz,sz);
		}
		catch(err)
		{
			var ti = (x-Math.floor(cell_sz/2))/cell_sz;
			var tj = (y-Math.floor(cell_sz/2))/cell_sz;
			alert(img+" "+ti+","+tj+"->"+grid[ti][tj]);
		}
		ctx.rotate(-ang);
		ctx.translate(-x,-y);

	}
	function paint_Lines(col)
	{
		var tmp = document.getElementById("myCanvas");
		ctx.fillStyle=col;
		for(var i=0; i<=grid_sz; ++i)
        {
			//for(var j=0; j<50; ++j)
				ctx.fillRect(i*cell_sz, 0, 1, tmp.height);
				ctx.fillRect( 0, i*cell_sz, tmp.width, 1);
        }
	}
