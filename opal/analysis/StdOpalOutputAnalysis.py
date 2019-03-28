class StdOpalOutputAnalysis:
    
    def calcRFphases(self, RFcavity):
        """
        Calculate the phases of individual cavities in the simulation
        

        Parameters
        ----------
        RFcavity    ([str])         name of the RFcavity as specifed in the input file
        
        Returns
        -------
        phases
        
        References
        ----------
        none

        Examples
        --------
        Check Cyclotron.ipynb in the opal/test directory
        """
        import re
        
        out_phases = []
        
        for i, cname in enumerate(RFcavity):
            turnNumber = 1
            file = open(self.ds.filename, "r")
            turns  = []
            phases = []
            for line in file:
                if re.search("Finished turn", line):
                    turnNumber += 1
                if re.search(cname, line):
                    phase = float(line.split()[5])
                    turns.append(turnNumber)
                    phases.append(phase)
            out_phases.append([turns,phases])
            file.close()
        
        return out_phases
