
package insa.lesirreductibles.PlotRadar.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("") 


public class PlotRessource {
	
	@GetMapping("/graph") 
	public String getInfos() { 
		return "<h1>Ploting Radar Graph</h1><div>localhost:8080/graph/YY-MM-DD-HH:mm_YY-MM-DD-HH:mm/AI/AA</div><div><a href=\"localhost:8080/graph/20-07-29-10:00_20-07-29-12:00/EVX02EK/38173A\">localhost:8080/graph/20-07-29-10:00_20-07-29-12:00/EVX02EK/38173A</div>";
        } 
	@GetMapping("/graph/{dates}/{ai}/{aa}") 
	public String getTrajectory(@PathVariable("dates") String dates,@PathVariable("ai") String ai,@PathVariable("aa") String aa) throws IOException, InterruptedException{ 
	dates = dates.replace("_"," ");
	//String command = "cmd.exe /c E:/eDocuments/\"projet intégrateur\"/plot_radar_microservice/scripts/plotRadar2.py 01:00:5e:50:00:26 12-12-2020 4841AA TRA39U"; 
	        String command = "python3 /home/user/Documents/plot_radar_microservice/scripts/plotRadar.py 25 "+dates+" "+ai+" "+aa; //01:00:5e:50:00:26 
                Process p = Runtime.getRuntime().exec(command); 
     	p.waitFor();  
     	String pathResult = "";
        try (BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()))) {                                
            String line;                                                                                                         
            while ((line = br.readLine()) != null)  {                                                                            
               System.out.println(line); 
               pathResult += line;
            }                                                                                                                    
        } 

		return "<div><b>Dates</b> : "+dates+"</div><div><b>AI</b> : "+ai+"</div><div><b>AA</b> : "+aa+"</div><div>"+pathResult+"</div>"; 
	} 



}
