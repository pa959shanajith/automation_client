var source = $("#ajax-comment").html();

Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
  return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
});

Handlebars.registerHelper('ifnotEquals', function(arg1, arg2, options) {
  return (arg1 != arg2) ? options.fn(this) : options.inverse(this);
});

Handlebars.registerHelper('getStyle', function(StepDescription) {
  if (StepDescription && (StepDescription.indexOf("Testscriptname") !== -1 || StepDescription.indexOf("TestCase Name") !== -1)) return "bold";
  else return;
});

Handlebars.registerHelper('getClass', function(StepDescription) {
  if (StepDescription && (StepDescription.indexOf("Testscriptname") !== -1 || StepDescription.indexOf("TestCase Name") !== -1)) return "collapsible-tc demo1 txtStepDescription";
  else return "rDstepDes tabCont";
});

Handlebars.registerHelper('getColor', function(overAllStatus) {
	if(overAllStatus == "Pass") return "green";
	else if(overAllStatus == "Fail")    return "red";
	else if(overAllStatus == "Terminate")    return "#faa536";
});

Handlebars.registerHelper('validateImageID', function(path, slno) {
  return path? ("#img-" + slno) : '';
});

Handlebars.registerHelper('validateImagePath', function(path) {
	return path ? 'block' : 'none';
});

Handlebars.registerHelper('getDataURI', function(uri) {
	var f="data:image/PNG;base64,";
  if (!uri || uri == "fail" || uri == "unavailableLocalServer") return f;
	else return f+uri;
});

var template = Handlebars.compile(source);

function toDataUrl(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
            callback(reader.result);
        }
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}

function adddetails(obj){
	data = obj.rows;
	var pass = fail = terminated = incomplete = P = F = T = I = 0;
	var total = data.length;
	var browserIcon, brow="";
	var styleColor, exeDate, exeDat, exeTime;
	for(i=0; i<data.length; i++){

		if(data[i].status == "Pass"){	pass++;}
		else if(data[i].status == "Fail"){	fail++;}
		else if(data[i].status == "Terminate"){	terminated++;}
		else if(data[i].status == "Incomplete"){	incomplete++;}
		else{pass++;}
		// exeDate = data[i].executedtime.split(" ")[0].split("-");
		// exeDat = ("0" + exeDate[0]).slice(-2) +"-"+ ("0" + exeDate[1]).slice(-2) +"-"+ exeDate[2];
		// var fst = data[i].executedtime.split(" ")[1].split(":");
		// exeTime = ("0" + fst[0]).slice(-2) +":"+ ("0" + fst[1]).slice(-2);
	}
	if(data.length > 0){
		P = parseFloat((pass/total)*100).toFixed();
		F = parseFloat((fail/total)*100).toFixed();
		T = parseFloat((terminated/total)*100).toFixed();
		I = parseFloat((incomplete/total)*100).toFixed();
		obj.overallstatus[0].pass = P;
		obj.overallstatus[0].fail = F;
		obj.overallstatus[0].terminate = T;
		obj.overallstatus[0].incomplete = I;
	}
	return obj;

}


$.getJSON("report.json",function(data){
	//data1 = adddetails(data);
	var dat = template(data);
	$("#maincontainer1").append(dat);   
	$('.ss').each(function(i,elem){
		$('#'+$($("[num='img-"+i+"']")[0]).attr('num')).attr('src',$(elem).text());
	})	

/*
	var generate = function(){
		var doc = new jsPDF();          
		var elementHandler = {
		  '#ignorePDF': function (element, renderer) {
			return true;
		  }
		};
		var source = window.document.getElementsByTagName("body")[0];
		doc.fromHTML(
			source,
			15,
			15,
			{
			  'width': 180,'elementHandlers': elementHandler
			});

		doc.output("dataurlnewwindow");
		
	};

	setTimeout(generate, 500);
*/	
});
