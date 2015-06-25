
	var array =new Array();
	var ValArray =new Array();
	var InaArray =new Array();
	require([
			"dojo/ready",
			"dojo/query",
			"dojo/parser",
			"dijit/layout/BorderContainer",
			 "dijit/layout/ContentPane"
		],function(ready, query,parser){			
			ready(function(){
				parser.parse();
				divMenuItemClick();
				
				dojo.byId("myFrame").onload = function()
				{
					var frameDoc = dojo.byId("myFrame").contentWindow.document;	
					if(frameDoc.title.toString() == "404 Not Found")
					{
						onerrorfunction();
					}else
					{	
						dojo.withDoc(frameDoc, function()
						{
							var dt = dojo.query("dt");
							var ddLog= dojo.query(".comment");							
							var dd= dojo.query("dd");							
							getDt(dt);
							getDd(dd);
						});

						array.sort(sortArray('author',false));
						array =  clearArray(array);		
						array = versionEm(array);												
						listAuthors();					
					}					
			}
			  });
			  
		//write author name				
			function listAuthors(){
				var authorContainer = dojo.byId("divAuthors");
					id ='"author_"';
					var tmp = '<div  id= ' + id + 'class=\"author\"><div>author_</div></div>';
					var html = "";				
				for(var index =0;index<array.length;index++)
				{						
					var author = array[index]["author"];
					html += tmp.replace(/author_/g,author);
					authorContainer.innerHTML = html;
					query(".author").on("click", function()
					{
						
						setContent(this.id);
						dojo.byId(this.id).style.color="blue";
						
					});
				}				
			}

			//显示统计结果
		function setContent(nodeId){
			var valiHtml="<div style=\"float:left;\">",invaliHtml ="<div style=\"float:left;\">",v = "";
			var countHtml="<div style=\"float:left;\">";
			var href = "http://glue.spolo.org/trac/glue/changeset/"+v+"/glue";
					
			for( var index =0;index<array.length;index++)
			{
				if( array[index]["author"] == nodeId)
				{
					v = array[index]["versionVal"].split(",");
					vLog = array[index]["logDetaiVal"];
					divLog = array[index]["logDetaiIna"];
					  div = array[index]["versionInval"].split(",");
					var ValCount = vLog.childNodes.length/2;
					var divCount = divLog.childNodes.length/2;
												
					countHtml += "<div style=\"float:left;margin-left:30px\"><p>总效提交次数： "
						+( parseInt(ValCount)+parseInt(divCount))
						+ "</p></div>"; 							
					countHtml += "<div style=\"float:left;margin-left:30px\"><p>无效提交次数： "
						+ divCount
						+ "</p></div>";
							
					countHtml += "<div style=\"float:left;margin-left:30px\"><p>有效提交次数： "
						+ ValCount
						+ "</p></div>"; 		
						
						countHtml += "<br/><div style=\"float:left;margin-left:30px\"><p>总提交代码行数： "
						+(array[index]["valCount"]+array[index]["invaCount"]).toString() 
						+ "</p></div>";	
					countHtml += "<div style=\"float:left;margin-left:30px\"><p>无效代码行数： "
						+ array[index]["invaCount"].toString() 
						+ "</p></div>"; 								
					countHtml += "<div  style=\"float:left;margin-left:30px\"><p >有效代码行数： "
							 + array[index]["valCount"].toString()
							 + "</p></div>"; 		
							 
					valiHtml += "<br><br>"+vLog.innerHTML;              
					invaliHtml += "<br><br>"+divLog.innerHTML;						
				}else{
						dojo.byId(array[index]["author"]).style.color = "#888";
					}
			}
			
			dojo.byId("count").innerHTML= countHtml ;
			dojo.byId("divInvalidRevision").innerHTML="<hr/><div><p>无效提交:</p></div>"+invaliHtml;
			dojo.byId("validRevision").innerHTML="<hr/><div><p>有效提交:</p></div> "+valiHtml;	
			
			var version = query(".revisionNumberInner");
			dojo.forEach(version, function(cell){
				var aHtml = "<a target=\"_blank\" href=\"http://glue.spolo.org/trac/glue/changeset/" +cell.innerHTML + "/glue\">";
				aHtml +=cell.innerHTML;
				aHtml += "<a/>";
					cell.innerHTML = aHtml;
			});
			
		}
			//get author and version
		function getDt(node){
			var k = -2;
			dojo.forEach(node, function(cell)
			{
				var logDetaiIna = document.createElement("div");
				var logDetaiVal = document.createElement("div");

			var list = {
				"version":"",
				"logDetaiIna":logDetaiIna,
				"logDetaiVal":logDetaiVal
				} ;
				list["logDetai0"] = document.createElement("dt");						
				if(cell.childNodes.length > 1){
					list["logDetai0"] = cell;						
				for(var index=0;index<cell.childNodes.length;index++)
				{						
					if(cell.childNodes[index].nodeName !="#text")
					{														
						if(cell.childNodes[index].href && cell.childNodes[index].href.indexOf("#") == -1) 
						{
							list["author"] = cell.childNodes[index].innerHTML;
						}									
						if(cell.childNodes[index].firstElementChild)
						{
							list["version"]= cell.childNodes[index].firstElementChild.innerHTML;								
						}									
						if(cell.childNodes.length <10)
						{
							list["version"]="";			
						}																								
					}
					array[k] = list;
					}
				}
				k++;
			}, this);				
		}				
						
			//get version
		function getDd(node){
			var k =-2;
			var flag =true;
		
		dojo.forEach(node, function(cell)
		{
			for(var index=0;index<cell.childNodes.length;index++)
			{
				if(cell.childNodes[index].nodeName !="#text" )
				{
					if(cell.childNodes[index].className == "comment"){  //获取log信息

                        // 虽然规范中规定的使用`sp:autocreated`，但是有人错误的写成了非ed形式
                        // 所以为了兼容这类错误，判断的地方不添加ed形式了。
                        // besides 如下形式“sp:autocrated”和“sp:autocreat” and so on.
						if(
                            cell.childNodes[index].innerHTML.indexOf("sp:auto") >-1 ||
                            cell.childNodes[index].innerHTML.indexOf("sp:created") >-1 ||
                            cell.childNodes[index].innerHTML.indexOf("sp:aotu") >-1
                        ) {
							array[k]["versionInval"] = array[k]["version"] ;
							array[k]["versionVal"] = "" ;
							flag=false;
						}else{
							array[k]["versionVal"] = array[k]["version"];
							array[k]["versionInval"] = "" ;
							flag=true;
						}							
					}
					if(cell.childNodes[index].firstElementChild && cell.childNodes[index].innerHTML.indexOf("<strong")  == 0){
						if(flag){
							array[k]["valCount"]  = parseInt(cell.childNodes[index].firstElementChild.innerHTML);
							array[k]["invaCount"]  = 0;

							//保存logdetail内容																
							ValArray.push(array[k]["author"],[array[k]["logDetai0"],cell]);
						}else{
							array[k]["valCount"] = 0;
							array[k]["invaCount"] = parseInt(cell.childNodes[index].firstElementChild.innerHTML);
							
							//保存logdetail内容
							InaArray.push(array[k]["author"],[array[k]["logDetai0"],cell]);
						}														
					}									
				}
				}
			k++;					
			}, this);	
		}							
});
		
		//改变日期 修改frame内容	
		function divMenuItemClick(){
		
			array =[];
			ValArray =[];
			InaArray =[];			
			clearsDiv("count");
			clearsDiv("divAuthors");
			clearsDiv("divInvalidRevision");
			clearsDiv("validRevision");
			var iframe= document.getElementById("myFrame");
			iframe.style.display = "block";
			iframe.style.height = "768px";
			iframe.style.width = "1024px";
			iframe.style.display = "none";
			
			//获取当前年月
			var myDate = new Date();
			var year =  document.getElementById("selectYear").value; 
			var month = document.getElementById("selectMonth").value; 
			var date = year + "-" + month;			 
			var curr_month = myDate.getMonth() + 1; // getMonth (0~11)
            
      if ( curr_month == month )
      {
        iframe.src = "./glue/commitlog.html";
      }
      else
      {
        iframe.src = "./glue/" + date + ".html";
      }
		}		
		
		//去掉重复author
		function clearArray(array){
			var len=array.length;
			for(var i =len-1;i>0;i--)
			{
				if(array[i-1]["author"] == array[i]["author"])
				{						
					addGroupJson(array[i-1], array[i]);
					array.splice(i,1); 	
				}					
			}			
			return array;
	}
		
		//按首字母排序
		function  sortArray(field, reverse){ 
			reverse = (reverse) ? -1 : 1; 
			return function(a,b){ 
				var f = a[field].localeCompare(b[field]); 
				if (f < 0){
					return reverse * -1; 
				}
				if(f > 0){ 
					return reverse * 1; 
				} 
				return 0; 
			} 
		}

		//合并json对象进行
		//数字求和
		//版本追加
		function addGroupJson(targetJson, packJson){
			var sp = ","
			if(targetJson && packJson){
			  for(var p in packJson){
				if(p == "author") 
				{
					continue;
				}else
					if(p.indexOf("version") > -1)
					{
						if(packJson[p])
						{
							sp = !targetJson[p]?"":",";
							targetJson[p] = targetJson[p]+sp+packJson[p];
						}
					}
					else if(p.indexOf("log") > -1)
					{
						continue;
					}else 
						targetJson[p]=parseInt(targetJson[p])+parseInt(packJson[p]);
				}
			  }
		}

		function versionEm(array){
			var len = array.length;
			for(var i = 0 ; i<len; i++){														
				for(var j = 0; j<InaArray.length; j++){
					var author_tmp =InaArray[j];
					var author_arr = array[i]["author"];
					if(author_arr == author_tmp){   
						try{
							array[i]["logDetaiIna"].appendChild(InaArray[j+1][0]);
							array[i]["logDetaiIna"].appendChild(InaArray[j+1][1]);
						}catch(err){
							console.log("0.1error");
						}                                                  
					}
				}
									
				for(var k = 0;k<ValArray.length;k++){
					var name_temp = ValArray[k];
					var name_arr = array[i]["author"];
					if( name_temp == name_arr){
						try{
							  array[i]["logDetaiVal"].appendChild(ValArray[k+1][0]);
							  array[i]["logDetaiVal"].appendChild(ValArray[k+1][1]);
							}catch(err){
							  console.log("error");
							}                             
					}
				}
			}
			return array;
		}
		
		function clearsDiv(nodeId){
			dojo.byId(nodeId).innerHTML="";
		}	
		
		function onerrorfunction(){
			alert("      Error 404, 没有可返回数据!");		
		}
