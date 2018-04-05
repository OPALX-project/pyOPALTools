
def calcTurnSeparation(ds):
    """ 
    Calculate turn separation from OPAL xxx--trackOrbit.dat file

    Parameters
    ----------
    ds      (DatasetBase)   datasets of type FileType.TRACK_ORBIT
    
    Returns
    -------
    none
    
    References
    ----------
    none

    Examples
    --------
    Check testCycl-1.py in the test directory
    
    Returns
    -------
    turn separation, energy, phi_r and radius
    """
    
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    x = ds.getData('x')
    y = ds.getData('y')
    px = ds.getData('px')
    py = ds.getData('py')
    pz = ds.getData('pz')
    
    # Get x-axis crossings
    pksx = detect_peaks(x, mph=0.04, mpd=100)
    mx = x[pksx]

    # Turn separation is the difference between crossings
    ts = np.diff(mx)

    # Particle energy
    p_mass = 938.28 # proton mass in MeV / c^2
    # Beta*gamma
    beta_gamma = np.sqrt(px * py + py * py + pz * pz)
    # Gamma
    gamma = np.sqrt(1+beta_gamma*beta_gamma)
    # Energy
    energy = (gamma - 1) * p_mass
    # Radius
    radius = np.sqrt( x * x + y * y)
    # Radial direction v_r (normalise with momentum?)
    phi_r = np.arctan( px / py ) - np.arctan( y / x )
    
    # Mask
    energy = energy[pksx]
    radius = radius[pksx]
    phi_r  = phi_r[pksx]
    
    return ts, energy, phi_r, radius


def calcCenteringExtraction(radius, turnCorrection=1.35,phaseCorrection=0.0,amplitudeCorrection=1):
    """
    Calculate betatron tune values and zentrierung

    Based on Fortran routine from Martin Humbel
    "Bestimmung der horizontalen Betatronschwingungsgroessen R0, DR, A und B mit der Methode der Normalengleichung"

    Parameters
    ----------
    radius
    turnCorrection      : Betatron oscillations per turn (tune), default value based on PSI Ring
    phaseCorrection     : Phase correction for betatron calculation in grad (radial angle between measurement and extraction)
    amplitudeCorrection : Amplitude correction for betatron calculation

    
    Examples
    --------
    TODO
    
    Returns
    -----
    the centering
    """
    
    # Use last 7 turns
    totalTurns = len(radius)
    turnsToAnalyse = min(7,totalTurns)
     
    centering = np.zeros(4) # R0, DR, sine (aka E), cosine (aka F)
    if (turnsToAnalyse < 2):
        return

    # Fill matrix
    dim = 4
    A = np.zeros((dim,dim))
    B = np.zeros(dim)
    for i in range(0,turnsToAnalyse):
        turnsFromExtraction = i - totalTurns + 1;
        turnNumber          = totalTurns - turnsToAnalyse + i;
        sinq = np.sin(turnsFromExtraction * 2 * np.pi * turnCorrection)
        cosq = np.cos(turnsFromExtraction * 2 * np.pi * turnCorrection)
        A[0][0] += 1
        A[0][1] += turnsFromExtraction
        A[0][2] += cosq
        A[0][3] += sinq
        A[1][1] += turnsFromExtraction * turnsFromExtraction
        A[1][2] += turnsFromExtraction * cosq
        A[1][3] += turnsFromExtraction * sinq
        A[2][2] += cosq * cosq
        A[2][3] += cosq * sinq
        A[3][3] += sinq * sinq

        B[0] += radius[turnNumber]
        B[1] += radius[turnNumber] * turnsFromExtraction
        B[2] += radius[turnNumber] * cosq
        B[3] += radius[turnNumber] * sinq

    # Make A symmetric
    for i in range(0,dim):
        for j in range(i+1,dim):
            A[j][i] = A[i][j]
    
    # No solution for 3 and 4 turns
    if (turnsToAnalyse == 3 or turnsToAnalyse == 4):
        centering[0] = radius[turnsToAnalyse-1]
        centering[1] = radius[turnsToAnalyse-1] - radius[turnsToAnalyse-2]
        return
    
    # Solve linear equations Ax = B
    (lu,piv)  = sp.linalg.lu_factor(A)
    centering = sp.linalg.lu_solve((lu,piv),B)
    
    # Correction factors
    phaseCorrInRad = phaseCorrection * np.pi / 180.;
    centering[0] = centering[0]
    centering[1] = centering[1]
    centering[2] = amplitudeCorrection * ( centering[2]*np.cos(phaseCorrInRad) + centering[3]*np.sin(phaseCorrInRad))
    centering[3] = amplitudeCorrection * (-centering[2]*np.sin(phaseCorrInRad) + centering[3]*np.cos(phaseCorrInRad))
    print 'Centering values [R0,DR,E,F] =',centering
    return centering
