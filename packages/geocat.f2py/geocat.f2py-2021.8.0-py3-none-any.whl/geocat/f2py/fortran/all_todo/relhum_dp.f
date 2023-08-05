C relative humidity [%]
      DOUBLE PRECISION FUNCTION DRELHUM(T,W,P)
      IMPLICIT NONE

c NCL function: rh = relhum (t,w,p)

C input

C temperature  [K]
      DOUBLE PRECISION T
C mixing ratio [kg/kg]
      DOUBLE PRECISION W
C pressure     [Pa]
      DOUBLE PRECISION P

c This is built from CCM Processor routines:
c     subroutine crlhmp1(w,t,mlon,mlon,klvl,p,rh)
c     subroutine estbl0b(ES,T)
C
C** NAME=ESBL0B
C
C     TABLE OF ES FROM -100 TO +102 C IN ONE-DEGREE INCREMENTS.
C
      DOUBLE PRECISION TABL1(82),TABL2(122)
      DOUBLE PRECISION TABLE(204)
      EQUIVALENCE (TABL1(1),TABLE(1)), (TABL2(1),TABLE(83))
      DATA TABL1/.01403D0,.01719D0,.02101D0,.02561D0,.03117D0,.03784D0,
     +     .04584D0,.05542D0,.06685D0,.08049D0,.09672D0,.1160D0,.1388D0,
     +     .1658D0,.1977D0,.2353D0,.2796D0,.3316D0,.3925D0,.4638D0,
     +     .5472D0,.6444D0,.7577D0,.8894D0,1.042D0,1.220D0,1.425D0,
     +     1.662D0,1.936D0,2.252D0,2.615D0,3.032D0,3.511D0,4.060D0,
     +     4.688D0,5.406D0,6.225D0,7.159D0,8.223D0,9.432D0,10.80D0,
     +     12.36D0,14.13D0,16.12D0,18.38D0,20.92D0,23.80D0,27.03D0,
     +     30.67D0,34.76D0,39.35D0,44.49D0,50.26D0,56.71D0,63.93D0,
     +     71.98D0,80.97D0,90.98D0,102.1D0,114.5D0,128.3D0,143.6D0,
     +     160.6D0,179.4D0,200.2D0,223.3D0,248.8D0,276.9D0,307.9D0,
     +     342.1D0,379.8D0,421.3D0,466.9D0,517.0D0,572.0D0,632.3D0,
     +     698.5D0,770.9D0,850.2D0,937.0D0,1032.0D0,1146.6D0/
      DATA TABL2/1272.0D0,1408.1D0,1556.7D0,1716.9D0,1890.3D0,2077.6D0,
     +     2279.6D0,2496.7D0,2729.8D0,2980.0D0,3247.8D0,3534.1D0,
     +     3839.8D0,4164.8D0,4510.5D0,4876.9D0,5265.1D0,5675.2D0,
     +     6107.8D0,6566.2D0,7054.7D0,7575.3D0,8129.4D0,8719.2D0,
     +     9346.5D0,10013.D0,10722.D0,11474.D0,12272.D0,13119.D0,
     +     14017.D0,14969.D0,15977.D0,17044.D0,18173.D0,19367.D0,
     +     20630.D0,21964.D0,23373.D0,24861.D0,26430.D0,28086.D0,
     +     29831.D0,31671.D0,33608.D0,35649.D0,37796.D0,40055.D0,
     +     42430.D0,44927.D0,47551.D0,50307.D0,53200.D0,56236.D0,
     +     59422.D0,62762.D0,66264.D0,69934.D0,73777.D0,77802.D0,
     +     82015.D0,86423.D0,91034.D0,95855.D0,100890.D0,106160.D0,
     +     111660.D0,117400.D0,123400.D0,129650.D0,136170.D0,142980.D0,
     +     150070.D0,157460.D0,165160.D0,173180.D0,181530.D0,190220.D0,
     +     199260.D0,208670.D0,218450.D0,228610.D0,239180.D0,250160.D0,
     +     261560.D0,273400.D0,285700.D0,298450.D0,311690.D0,325420.D0,
     +     339650.D0,354410.D0,369710.D0,385560.D0,401980.D0,418980.D0,
     +     436590.D0,454810.D0,473670.D0,493170.D0,513350.D0,534220.D0,
     +     555800.D0,578090.D0,601130.D0,624940.D0,649530.D0,674920.D0,
     +     701130.D0,728190.D0,756110.D0,784920.D0,814630.D0,845280.D0,
     +     876880.D0,909450.D0,943020.D0,977610.D0,1013250.D0,
C*PL*ERROR* Too many continuation lines generated
     +     1049940.D0,1087740.D0,1087740.D0/

      DOUBLE PRECISION TP,T2,ES
      INTEGER IT

      TP = T
      IF (TP.GT.375.16D0) TP = 375.16D0
      IF (TP.LT.173.16D0) TP = 173.16D0
      IT = TP - 173.16D0
      T2 = 173.16D0 + IT
      ES = (T2+1.D0-TP)*TABLE(IT+1) + (TP-T2)*TABLE(IT+2)
      ES = ES*1.0D-01

      DRELHUM = (W* (P-0.378D0*ES)/ (0.622D0*ES))*100.D0

C There is some discussion about whether the humidities
C should be allowed to be above 100%. Right now, we're
C leaving the code as is. We may eventually comment
C this line out, or create another function.
C
C Dennis decided to comment this line out for V5.2.0.
C
C      IF (DRELHUM.GT.100.D0) DRELHUM = 100.D0
      IF (DRELHUM.LT.0.D0)   DRELHUM = 0.0001D0

      RETURN
      END
