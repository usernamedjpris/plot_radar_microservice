package insa.lesirreductibles.PlotRadar.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/graph") 
public class PlotRessource {
	
	@GetMapping("/{aaai}") 
	public String getTrajectory(@PathVariable("aaai") String id) throws IOException, InterruptedException{ 
		
	//String command = "cmd.exe /c E:/eDocuments/\"projet intégrateur\"/plot_radar_microservice/scripts/plotRadar2.py 01:00:5e:50:00:26 12-12-2020 4841AA TRA39U"; 
	        String command = "python3 /home/user/Documents/plot_radar_microservice/scripts/plotRadar.py 01:00:5e:50:00:26 20-07-29-10:00 20-07-29-12:00 EVX02EK 38173A" 	;
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

		return pathResult; 
	} 
}
