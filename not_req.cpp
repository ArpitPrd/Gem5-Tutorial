#include <stdio.h>
#define UNROLL (4)
#define BLOCKSIZE 32
#define N 70

// void do_block (int n, int si, int sj, int sk, double *A, double *B, double *C) {
//     for ( int i = si; i < si+BLOCKSIZE; i+=UNROLL*4 ) {
//         for ( int j = sj; j < sj+BLOCKSIZE; j++ ) {
//             /*using 4 bytes for double storage*/
//             __m256d c[4];
//             for ( int x = 0; x < UNROLL; x++ ){
//                 /*accessing the in the linear array*/
//                 c[x] = _mm256_load_pd(C+i+x*4+j*n);
//             }
//             for( int k = sk; k < sk+BLOCKSIZE; k++ ) {
//                 /*accessing b in the linear array*/
//                 __m256d b = _mm256_broadcast_sd(B+k+j*n);
//                 for (int x = 0; x < UNROLL; x++){
//                     /* performing matrix multiplication */
//                     c[x] = _mm256_add_pd(c[x], /* c[x]+=A[i][k]*b */_mm256_mul_pd(_mm256_load_pd(A+n*k+x*4+i), b));
//                 }
//             }

//             for ( int x = 0; x < UNROLL; x++ ){
//                 _mm256_store_pd(C+i+x*4+j*n, c[x]);
//             }
//         }
//     }
// }

// void dgemm (int n, double* A, double* B, double* C) {
//     for ( int sj = 0; sj < n; sj += BLOCKSIZE )
//         for ( int si = 0; si < n; si += BLOCKSIZE )
//             for ( int sk = 0; sk < n; sk += BLOCKSIZE )
//                 do_block(n, si, sj, sk, A, B, C);
// }

// void mat_mul_full(double* A, double* B, double* C) {
//     for ( int sj = 0; sj < N; sj += BLOCKSIZE )
//         for ( int si = 0; si < N; si += BLOCKSIZE )
//             for ( int sk = 0; sk < N; sk += BLOCKSIZE )
//                 for ( int i = si; i < si+BLOCKSIZE; i+=UNROLL*4 ) {
//                     for ( int j = sj; j < sj+BLOCKSIZE; j++ ) {
//                         /*using 4 bytes for double storage*/
//                         __m256d c[4];
//                         for ( int x = 0; x < UNROLL; x++ ){
//                             /*accessing the in the linear array*/
//                             c[x] = _mm256_load_pd(C+i+x*4+j*N);
//                         }
//                         for( int k = sk; k < sk+BLOCKSIZE; k++ ) {
//                             /*accessing b in the linear array*/
//                             __m256d b = _mm256_broadcast_sd(B+k+j*N);
//                             for (int x = 0; x < UNROLL; x++){
//                                 /* performing matrix multiplication */
//                                 c[x] = _mm256_add_pd(c[x], /* c[x]+=A[i][k]*b */_mm256_mul_pd(_mm256_load_pd(A+N*k+x*4+i), b));
//                             }
//                         }

//                         for ( int x = 0; x < UNROLL; x++ ){
//                             _mm256_store_pd(C+i+x*4+j*N, c[x]);
//                         }
//                     }
//                 }
// }

double get_el(double *mat, int i, int j) {
    return *(mat + i*(N) + j);
}

double *point_to_el(double *A, int i, int j) {
    return A + i *(N) + j;
}

void print(int n, double *A) {
    for (int i=0; i <n; i++) {
        printf("\t");
        for (int j=0; j<n; j++) {
            printf("%f ", get_el(A, i, j));
        }
        printf("\n");
    }
}

/**
 * @brief transpose in place
 */
void transpose(double * A) {
    for (int i=0; i<N; i++) {
        for (int j=i+1; j<N; j++) {
            double tmpij = get_el(A, i, j);
            double tmpji = get_el(A, j, i);
            *(point_to_el(A, i, j)) = tmpji;
            *(point_to_el(A, j, i)) = tmpij;
        }
    }
}

void mat_mul_no_cache(int n, double *A, double *B, double *C) {
    transpose(B);
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            *(point_to_el(C, i, j)) = 0.;
            for (int k=0; k<n; k++) {
                *(point_to_el(C, i, j)) += get_el(A, i, k) * get_el(B, j, k);
            }
        }
    }
}
