/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

#include "mm_basics.h"

// %%EXPORT_KWD MM_BASICS_API


// %%GEN h
// %%GEN c



// %%GEN ch
#ifdef __cplusplus
extern "C" {
#endif
// %%GEN c

//  %%GEN h
//  %%GEN c


#define END_WORD 0xffffffff

static inline void mm_group_iter_next_atom(mm_group_iter_t *pit)
{
    uint32_t result;
    if (pit->e == 0)  {
        pit->lookahead = END_WORD;
        return;
    }
    result =  pit->g[pit->index];
    if ((pit->index += pit->i_step) == pit->i_stop) {
        pit->index = pit->i_start;
        --pit->e;
    }
    pit->lookahead = result ^ pit->sign;
}



// %%EXPORT 
MM_BASICS_API
void mm_group_iter_start(mm_group_iter_t *pit, uint32_t *g, int32_t len_g, int32_t e)
{
    pit->g = g;
    pit->e = e;
    if (len_g == 0) pit->e = 0;
    if (e >= 0) {
        pit->i_start = 0; pit->i_stop = len_g; pit->i_step = 1;
        pit->sign = 0;
    } else {
        pit->i_start = len_g - 1; pit->i_stop = pit->i_step = -1;
        pit->sign = 0x80000000;
        pit->e = -e;
    }
    pit->index = pit->i_start;
    pit->lookahead = 0;
}




// %%EXPORT 
MM_BASICS_API
uint32_t  mm_group_iter_next(mm_group_iter_t *pit)
{
    uint32_t atom, tag, i, xi_used, *g;

    g = pit->data + 1;
    for (i = 0; i < 6; ++i) pit->data[i] = 0;
    xi_used = 0;

    while (1)  {
        atom = pit->lookahead;
        tag = (atom >> 28) & 0xf;
        switch (tag) {
            case 8:
            case 0:
                break;
            case 8 + 1:
            case 1:
                mm_group_n_mul_delta_pi(g, atom & 0xfff, 0);
                xi_used = 1;
                break;
            case 8 + 2:
                mm_group_n_mul_inv_delta_pi(g, 0, atom & 0xfffffff);
                xi_used = 1;
                break;
            case 2:
                mm_group_n_mul_delta_pi(g, 0, atom & 0xfffffff);
                xi_used = 1;
                break;
            case 8 + 3:
                atom ^= MAT24_THETA_TABLE[atom & 0x7ff] & 0x1000;
            case 3:
                mm_group_n_mul_x(g, atom & 0x1fff);
                xi_used = 1;
                break;
            case 8 + 4:
                atom ^= MAT24_THETA_TABLE[atom & 0x7ff] & 0x1000;
            case 4:
                mm_group_n_mul_y(g, atom & 0x1fff);
                xi_used = 1;
                break;
            case 8 + 5:
                atom ^= 0xfffffff;
            case 5:
                mm_group_n_mul_t(g, atom & 0xfffffff);
                xi_used = 1;
                break;
            case 8 + 6:
                atom ^= 0xfffffff;
            case 6:              
                if (xi_used)  return 0;
                pit->data[0] = (pit->data[0] + (atom & 0xfffffff)) % 3;
                break;
            default:
                atom |= 0x80000000;
                if (atom == END_WORD) return 1; 
                if (atom == 0xf0000000) return pit->lookahead = 0;
                return 2;
        }
        mm_group_iter_next_atom(pit);
    }

}



//  %%GEN h
//  %%GEN c


// %%GEN ch
#ifdef __cplusplus
}
#endif
//  %%GEN c

