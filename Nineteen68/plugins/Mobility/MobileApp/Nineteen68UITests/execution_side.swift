//
//  execution_side.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 10/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import SwiftSocket
import SwiftyJSON
var bundle_id = ""
class execution_side{
    
    func execution(client:TCPClient)->[String] {
        
        
        //read keyword
        func read_keyword()->(String){
            var data = client.read(1)
            var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            var num=strnum!
            var len = Int(num.intValue)
            data = client.read(len)
            strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            num=strnum!
            len = Int(num.intValue)
            data = client.read(len)
            let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            let keyword = str! as String
            return keyword
        }
        //read label
        func read_label() ->(String) {
            var data=client.read(1)
            var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            var num=strnum!
            var len = Int(num.intValue)
            if len == 0 {
                return "0"
            }
            data = client.read(len)
            strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            num=strnum!
            len = Int(num.intValue)
            data = client.read(len)
            let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            let label = str! as String
            return label
        }
        
        
        //read label type
        func read_label_type() ->(String) {
            var data=client.read(1)
            var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            var num=strnum!
            var len = Int(num.intValue)
            if len == 0 {
                return "0"
            }
            data = client.read(len)
            strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            num=strnum!
            len = Int(num.intValue)
            data = client.read(len)
            let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            let label = str! as String
            return label
        }
        
        

        //read input
        func read_input()->(String){
        var data=client.read(1)
        var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
        var num=strnum!
        var len = Int(num.intValue)
            if len == 0 {
                return "0"
            }
        data = client.read(len)
        strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
        num=strnum!
        len = Int(num.intValue)
        data = client.read(len)
        let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
        let input = str! as String
            return input
        }
        
        
        
        let keyword = read_keyword()
       
        let label = read_label()
        
        let labeltype = read_label_type()
        
        let input = read_input()
         print(keyword,label,labeltype,input)
       
    

        var result : [String] = ["temp"]
        switch keyword {
      
        case "launchapplication": bundle_id = input ; result[0] = dispatch().get_value(bundle_id: input,action: "LaunchApplication");return result
            
        case "press": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "tap" , label : label,key : labeltype);return result
        case "presselement":result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "tap" , label : label,key : labeltype);return result
        case "toggleon":result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "tap" , label : label,key : labeltype);return result
        case "toggleoff":result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "tap" , label : label,key : labeltype);return result
            
        
        case "getstatus":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "getstatus" , label : label,key : labeltype);return result
        case "unselectcheckbox":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "unselectcheckbox" , label : label,key : labeltype);return result
        case "backpress":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "backpress" , label : label,key : labeltype);return result
        
       
        case "selectradiobutton": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "selectradiobutton" , label : label,key : labeltype);return result
        case "selectcheckbox": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "selectradiobutton" , label : label,key : labeltype);return result
            
            
            
            
        case "longpress" :result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "longpress",label: label,key: labeltype,forDuration: Double(input)!);return result
        case "longpresselement" :result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "longpress",label: label,key: labeltype,forDuration: Double(input)!);return result
  
        case "getbuttonname": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "getbuttonname", label : label,key: labeltype);return result
        case "getelementtext": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "getbuttonname", label : label,key: labeltype);return result
        
            

            
        case "swipeup":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "swipeup", label : label,key: labeltype);return result
        case "swipedown":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "swipedown", label : label,key: labeltype);return result
        case "swipeleft":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "swipeleft", label : label,key: labeltype);return result
        case "swiperight":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "swiperight", label : label,key: labeltype);return result
            
        
        case "verifybuttonname": result[0] = dispatch().get_value(bundle_id: bundle_id, action: "verifybuttonname", label : label,key: labeltype, input_text:input);return result
        case "verifyelementtext":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "verifybuttonname",label: label,key: labeltype,input_text: input);return result
            
            
        
        case "verifyelementexists":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementexists",label: label,key: labeltype));return result
        case "verifyelementdoesnotexists":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifydoesnotelementexists",label: label,key: labeltype));return result
        case "verifyexists":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementexists",label: label,key: labeltype));return result
        
        
        case "verifyhidden":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyhidden",label: label,key: labeltype));return result
        case "verifyvisible":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyvisible",label: label,key: labeltype));return result
        
        
        
        
        
        case "waitforelementexists":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "waitforelementexists",label: label,key: labeltype));return result

        
        
        case "verifyelementenabled":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementenabled",label: label,key: labeltype));return result
        case "verifyenabled":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementenabled",label: label,key: labeltype));return result
        case "verifyelementdisabled":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementdisabled",label: label,key: labeltype));return result
        case "verifydisabled":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifyelementdisabled",label: label,key: labeltype));return result
            
        case "verifytext":result[0] = (dispatch().get_value(bundle_id: bundle_id, action: "verifytext",label: label,key: labeltype,input_text: input));return result
        

        
        
        
        case "settext":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "type_text" , label : label,key : labeltype,input_text: input) ;return result
        case "sendvalue":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "type_text" , label : label,key : labeltype,input_text: input) ;return result
        
        case "setsecuretext":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "type_securetext" , label : label,key : labeltype,input_text: input);return result
            
            
            
        case "setslidevalue" :result[0] =  dispatch().get_value(bundle_id: bundle_id, action: "adjusting_Slider",label: label,key: labeltype,float_val: Float(input)!);return result
        
        case "doubletap":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "doubletap" , label : label,key : labeltype);return result
        case "cleartext":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "cleartext" , label : label,key : labeltype);return result
        case "gettext":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "gettext" , label : label,key : labeltype);return result
        
        case "getvalue":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "gettext" , label : label,key : labeltype);return result
        case "getslidevalue":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "gettext" , label : label,key : labeltype);return result
        case "setvalue":result[0] = dispatch().get_value(bundle_id: bundle_id, action: "setvalue" , label : label,key : labeltype,input_text: input);return result


        default:
            return(["no keyword found"])
        }
        
        
    }
    
    
}


