
var source = $("#ajax-comment").html();

Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
    return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
});

Handlebars.registerHelper('ifnotEquals', function(arg1, arg2, options) {
    return (arg1 != arg2) ? options.fn(this) : options.inverse(this);
});

Handlebars.registerHelper('getStyle', function(StepDescription) {
    if(StepDescription.indexOf("Testscriptname") !== -1 || StepDescription.indexOf("TestCase Name") !== -1) return "bold";
    else return;
});

Handlebars.registerHelper('getClass', function(StepDescription) {
    if(StepDescription.indexOf("Testscriptname") !== -1 || StepDescription.indexOf("TestCase Name") !== -1) return "collapsible-tc demo1 txtStepDescription";
    else return "rDstepDes tabCont";
});

Handlebars.registerHelper('getColor', function(overAllStatus) {
	if(overAllStatus == "Pass") return "green";
	else if(overAllStatus == "Fail")    return "red";
	else if(overAllStatus == "Terminate")    return "#faa536";
});

Handlebars.registerHelper('validateImageID', function(path,slno) {
	if(path!=null) return "#img-"+slno;
	else return '';
});

Handlebars.registerHelper('validateImagePath', function(path) {
	if(path!=null) return 'block';
	else return 'none';
});

Handlebars.registerHelper('getDataURI', function(uri) {
	var f="data:image/PNG;base64,";
	if(uri=="fail" || uri=="unavailableLocalServer") return f;
	else return f+uri;
});

var template = Handlebars.compile(source);
/*
var data1 = {
  "overallstatus": [
    {
      "domainName": "Manufacturing",
      "projectName": "Demo",
      "releaseName": "Demo",
      "cycleName": "Demo",
      "scenarioName": "Scenario_0demo",
      "browserVersion": "NA",
      "browserType": "NA",
      "StartTime": "2018-07-30 14:50:16",
      "EndTime": "2018-07-30 14:50:21",
      "overAllStatus": "Fail",
      "EllapsedTime": "~00:00:04",
      "date": "07/30/2018",
      "time": "14:50:21",
      "pass": "50.00",
      "fail": "50.00",
      "terminate": 0
    }
  ],
  "rows": [
    {
      "Comments": "",
      "StepDescription": "TestCase Name: Testcase_0demo",
      "id": 1,
      "Keyword": "TestCase Name",
      "parentId": 0,
      "slno": 1
    },
    {
      "status": "Fail",
      "Remark": "",
      "Keyword": "verifytextiris",
      "Step ": "Step 1",
      "EllapsedTime": "00:00:01:574",
      "testcase_details": {
        "actualResult_pass": "Chrome",
        "testcaseDetails": "Chrome1",
        "actualResult_fail": "Chrome"
      },
      "Comments": null,
      "screenshot_path": null,
      "StepDescription": " Verify 'Chrome1' is the text in the 'Chrometext'.",
      "parentId": 0,
      "id": 2,
      "slno": 2,
      "Step": "Step 1"
    },
    {
      "status": "Fail",
      "Remark": "",
      "Keyword": "verifyValues",
      "Step ": "Step 2",
      "EllapsedTime": "00:00:01:008",
      "testcase_details": {
        "actualResult_pass": "23451",
        "testcaseDetails": "2345",
        "actualResult_fail": "23451"
      },
      "Comments": null,
      "screenshot_path": null,
      "StepDescription": "Verify values '2345' and '23451' and save the result in ''.",
      "parentId": 0,
      "id": 3,
      "slno": 3,
      "Step": "Step 2"
    },
    {
      "status": "Pass",
      "Remark": "Â ",
      "Keyword": "verifytextiris",
      "Step ": "Step 3",
      "EllapsedTime": "00:00:01:291",
      "testcase_details": {
        "actualResult_pass": "Chrome",
        "testcaseDetails": "Chrome",
        "actualResult_fail": "Chrome"
      },
      "Comments": null,
      "screenshot_path": null,
      "StepDescription": " Verify 'Chrome' is the text in the 'Chrometext'.",
      "parentId": 0,
      "id": 4,
      "slno": 4,
      "Step": "Step 3"
    },
    {
      "status": "Pass",
      "Remark": "Â ",
      "Keyword": "verifyValues",
      "Step ": "Step 4",
      "EllapsedTime": "00:00:01:008",
      "testcase_details": {
        "actualResult_pass": "2345",
        "testcaseDetails": "2345",
        "actualResult_fail": "2345"
      },
      "Comments": null,
      "screenshot_path": null,
      "StepDescription": "Verify values '2345' and '2345' and save the result in ''.",
      "parentId": 0,
      "id": 5,
      "slno": 5,
      "Step": "Step 4"
    }
  ]
};
*/

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
		//$('#img-'+i).attr('src',$(elem).text());
	})	
/*		
	$('.ss').each(function(i,elem){
		toDataUrl($(elem).text(),function(data){
			$('#'+$($("[num='img-"+i+"']")[0]).attr('num')).attr('src',data);
			console.log(data);
			console.log('\n');
		})	
	});*/
	
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
