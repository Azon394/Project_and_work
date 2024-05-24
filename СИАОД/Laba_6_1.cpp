#include <glpk.h>

int main(void) {
    glp_prob *lp;
    int ia[1+1000], ja[1+1000];
    double ar[1+1000], z, x1, x2, x3;

    lp = glp_create_prob();
    glp_set_prob_name(lp, "sample");
    glp_set_obj_dir(lp, GLP_MAX);

    glp_add_rows(lp, 1);
    glp_set_row_name(lp, 1, "p");
    glp_set_row_bnds(lp, 1, GLP_UP, 0.0, 500.0);

    glp_add_cols(lp, 3);
    glp_set_col_name(lp, 1, "x1");
    glp_set_col_kind(lp, 1, GLP_IV);
    glp_set_col_bnds(lp, 1, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 1, 2/3.0 + 0);

    glp_set_col_name(lp, 2, "x2");
    glp_set_col_kind(lp, 2, GLP_IV);
    glp_set_col_bnds(lp, 2, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 2, 1/3.0 + 2/2.0);

    glp_set_col_name(lp, 3, "x3");
    glp_set_col_kind(lp, 3, GLP_IV);
    glp_set_col_bnds(lp, 3, GLP_LO, 0.0, 0.0);
    glp_set_obj_coef(lp, 3, 0 + 3/2.0);

    ia[1] = 1, ja[1] = 1, ar[1] = 1.0;
    ia[2] = 1, ja[2] = 2, ar[2] = 1.0;
    ia[3] = 1, ja[3] = 3, ar[3] = 1.0;

    glp_load_matrix(lp, 3, ia, ja, ar);

    glp_simplex(lp, NULL);
    glp_intopt(lp, NULL);

    z = glp_mip_obj_val(lp);
    x1 = glp_mip_col_val(lp, 1);
    x2 = glp_mip_col_val(lp, 2);
    x3 = glp_mip_col_val(lp, 3);

    printf("\nZ = %g; X1 = %g; X2 = %g; X3 = %g\n", z, x1, x2, x3);

    glp_delete_prob(lp);

    return 0;
}
