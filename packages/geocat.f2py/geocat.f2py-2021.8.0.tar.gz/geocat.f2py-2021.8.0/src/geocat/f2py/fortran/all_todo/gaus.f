      SUBROUTINE GAQDNCL(NLAT,THETA,WTS,WORK,LWORK,IERROR)
C     SUBROUTINE GAQDNCL COMPUTES GAUSSIAN POINTS (IN RADIANS) AND WEIGHTS
C     ON THE SPHERE IN THE INTERVAL (0,PI).  (THESE CAN BE USED IN
C     GAUSSIAN QUADRATURE FOR ESTIMATING INTEGRALS ON THE SPHERE)
C
C
C
C
      DIMENSION WORK(LWORK),THETA(NLAT),WTS(NLAT)
      DOUBLE PRECISION WORK,THETA,WTS,X
      N = NLAT
      IERROR = 1
C     CHECK WORK SPACE LENGTH
      IF (LWORK.LT.4*N*(N+1)+2) RETURN
      IERROR = 2
      IF (N.LE.0) RETURN
      IERROR = 0
      IF (N.GT.2) THEN
C     PARTITION WORK SPACE FOR DOUBLE PRECISION EIGENVALUE(VECTOR COMPUTATION)
      I1 = 1
      I2 = I1+2*N
      I3 = I2+2*N
      CALL GAQDNCL1(N,THETA,WTS,WORK(I1),WORK(I2),WORK(I3),IERROR)
      IF (IERROR.NE.0) THEN
      IERROR = 3
      RETURN
      END IF
      RETURN
      ELSE IF (N.EQ.1) THEN
      WTS(1) = 2.0D0
      THETA(1) = DACOS(0.0D0)
      ELSE IF (N.EQ.2) THEN
C     COMPUTE WEIGHTS AND POINTS ANALYTICALLY WHEN N=2
      WTS(1) = 1.0D0
      WTS(2) = 1.0D0
      X = DSQRT(1.0D0/3.0D0)
      THETA(1) = DACOS(X)
      THETA(2) = DACOS(-X)
      RETURN
      END IF
      END
      SUBROUTINE GAQDNCL1(N,THETA,WTS,W,E,WRK,IER)
      DIMENSION THETA(N),WTS(N),W(N),E(N),WRK(1)
      DOUBLE PRECISION THETA,WTS,TEMP,W,E,WRK
C     SET SYMMETRIC TRIDIAGNONAL MATRIX SUBDIAGONAL AND DIAGONAL
C     COEFFICIENTS FOR MATRIX COMING FROM COEFFICIENTS IN THE
C     RECURSION FORMULA FOR LEGENDRE POLYNOMIALS
C     A(N)*P(N-1)+B(N)*P(N)+C(N)*P(N+1) = 0.
      WRK(1)=0.D0
      WRK(N+1) = 0.D0
      W(1)=0.D0
      E(1) = 0.D0
      DO 100 J=2,N
      WRK(J)= (J-1.D0)/DSQRT((2.D0*J-1.D0)*(2.D0*J-3.D0))
      WRK(J+N)=0.D0
      E(J) = WRK(J)
      W(J) = 0.D0
  100 CONTINUE
C     COMPUTE EIGENVALUES  OF MATRIX
      MATZ = 1
      INDX = 2*N+1
      NP1=N+1
      CALL DRSTNCL(N,N,W,E,MATZ,WRK(INDX),IER)
      IF (IER.NE.0) RETURN
C     COMPUTE GAUSSIAN WEIGHTS AND POINTS
      DO 101 J=1,N
      THETA(J) = DACOS(W(J))
C     SET GAUSSIAN WEIGHTS AS 1ST COMPONENTS OF EIGENVECTORS SQUARED
      INDX = (J+1)*N+1
      WTS(J) = 2.0D0*WRK(INDX)**2
  101 CONTINUE
C     REVERSE ORDER OF GAUSSIAN POINTS TO BE
C     MONOTONIC INCREASING IN RADIANS
      N2 = N/2
      DO 102 I=1,N2
      TEMP = THETA(I)
      THETA(I) = THETA(N-I+1)
      THETA(N-I+1) = TEMP
  102 CONTINUE
      RETURN
      END


      SUBROUTINE DRSTNCL(NM,N,W,E,MATZ,Z,IERR)
C     DRSTNCL IS A DOUBLE PRECISION MODIFICATION OF RST OFF EISPACK
C     TO BE USED  TO COMPUTE GAUSSIAN POINTS AND WEIGHTS

C
      INTEGER I,J,N,NM,IERR,MATZ
      DOUBLE PRECISION W(N),E(N),Z(NM,N)

C
C     .......... FIND BOTH EIGENVALUES AND EIGENVECTORS ..........
   20 DO 40 I = 1, N
C
	 DO 30 J = 1, N
	    Z(J,I) = 0.0D0
   30    CONTINUE
C
	 Z(I,I) = 1.0D0
   40 CONTINUE
C
      CALL  DINTQLNCL(NM,N,W,E,Z,IERR)
      RETURN
      END

      SUBROUTINE DINTQLNCL(NM,N,D,E,Z,IERR)
C     DINTQLNCL IS A DOUBLE PRECISION MODIFICATION OF INTQL2 OFF
C     EISPACK TO BE USED BY GAQDNCL IN SPHEREPACK FOR COMPUTING
C     GAUSSIAN WEIGHTS AND POINTS
C
      INTEGER I,J,K,L,M,N,II,NM,MML,IERR
      DOUBLE PRECISION D(N),E(N),Z(NM,N)
      DOUBLE PRECISION B,C,F,G,P,R,S,TST1,TST2,DPYTHANCL
      IERR = 0
      IF (N .EQ. 1) GO TO 1001
C
      DO 100 I = 2, N
  100 E(I-1) = E(I)
C
      E(N) = 0.0D0
C
      DO 240 L = 1, N
	 J = 0
C     .......... LOOK FOR SMALL SUB-DIAGONAL ELEMENT ..........
C   
  105    NM1 = N-1     
         IF(L .GT. NM1) GO TO 111
         DO 110 MDO = L, NM1
            M = MDO
	    TST1 = DABS(D(M)) + DABS(D(M+1))
	    TST2 = TST1 + DABS(E(M))
	    IF (TST2 .EQ. TST1) GO TO 120
  110    CONTINUE
  111    M = N
C
  120    P = D(L)
	 IF (M .EQ. L) GO TO 240
	 IF (J .EQ. 30) GO TO 1000
	 J = J + 1
C     .......... FORM SHIFT ..........
	 G = (D(L+1) - P) / (2.0D0 * E(L))
	 R = DPYTHANCL(G,1.0D0)
	 G = D(M) - P + E(L) / (G + SIGN(R,G))
	 S = 1.0D0
	 C = 1.0D0
	 P = 0.0D0
	 MML = M - L
C     .......... FOR I=M-1 STEP -1 UNTIL L DO -- ..........
	 DO 200 II = 1, MML
	    I = M - II
	    F = S * E(I)
	    B = C * E(I)
	    R = DPYTHANCL(F,G)
	    E(I+1) = R
	    IF (R .EQ. 0.0D0) GO TO 210
	    S = F / R
	    C = G / R
	    G = D(I+1) - P
	    R = (D(I) - G) * S + 2.0D0 * C * B
	    P = S * R
	    D(I+1) = G + P
	    G = C * R - B
C     .......... FORM VECTOR ..........
	    DO 180 K = 1, N
	       F = Z(K,I+1)
	       Z(K,I+1) = S * Z(K,I) + C * F
	       Z(K,I) = C * Z(K,I) - S * F
  180       CONTINUE
C
  200    CONTINUE
C
	 D(L) = D(L) - P
	 E(L) = G
	 E(M) = 0.0D0
	 GO TO 105
C     .......... RECOVER FROM UNDERFLOW ..........
  210    D(I+1) = D(I+1) - P
	 E(M) = 0.0D0
	 GO TO 105
  240 CONTINUE
C     .......... ORDER EIGENVALUES AND EIGENVECTORS ..........
      DO 300 II = 2, N
	 I = II - 1
	 K = I
	 P = D(I)
C
	 DO 260 J = II, N
	    IF (D(J) .GE. P) GO TO 260
	    K = J
	    P = D(J)
  260    CONTINUE
C
	 IF (K .EQ. I) GO TO 300
	 D(K) = D(I)
	 D(I) = P
C
	 DO 280 J = 1, N
	    P = Z(J,I)
	    Z(J,I) = Z(J,K)
	    Z(J,K) = P
  280    CONTINUE
C
  300 CONTINUE
C
      GO TO 1001
C     .......... SET ERROR -- NO CONVERGENCE TO AN
C                EIGENVALUE AFTER 30 ITERATIONS ..........
 1000 IERR = L
 1001 RETURN
      END

      DOUBLE PRECISION FUNCTION DPYTHANCL(A,B)
      DOUBLE PRECISION A,B
C     DPYTHANCL IS A DOUBLE PRECISION MODIFICATION OF PYTHAG OFF EISPACK
C     FOR USE BY DIMTQL

C
C     FINDS SQRT(A**2+B**2) WITHOUT OVERFLOW OR DESTRUCTIVE UNDERFLOW
C
      DOUBLE PRECISION P,R,S,T,U
      P = DABS(A)
      IF (DABS(B).GE.DABS(A)) P = DABS(B)
C     P = AMAX1(DABS(A),DABS(B))
      IF (P .EQ. 0.0D0) GO TO 20
      R = (DABS(A)/P)**2
      IF (DABS(B).LT.DABS(A)) R = (DABS(B)/P)**2
C     R = (AMIN1(DABS(A),DABS(B))/P)**2
   10 CONTINUE
	 T = 4.0D0 + R
	 IF (T .EQ. 4.0D0) GO TO 20
	 S = R/T
	 U = 1.0D0 + 2.0D0*S
	 P = U*P
	 R = (S/U)**2 * R
      GO TO 10
   20 DPYTHANCL = P
      RETURN
      END


