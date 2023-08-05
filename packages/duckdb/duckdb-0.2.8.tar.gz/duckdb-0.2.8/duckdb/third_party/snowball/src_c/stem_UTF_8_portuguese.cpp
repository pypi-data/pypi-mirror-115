/* Generated by Snowball 2.0.0 - https://snowballstem.org/ */

#include "../runtime/header.h"

#ifdef __cplusplus
extern "C" {
#endif
extern int portuguese_UTF_8_stem(struct SN_env * z);
#ifdef __cplusplus
}
#endif
static int r_residual_form(struct SN_env * z);
static int r_residual_suffix(struct SN_env * z);
static int r_verb_suffix(struct SN_env * z);
static int r_standard_suffix(struct SN_env * z);
static int r_R2(struct SN_env * z);
static int r_R1(struct SN_env * z);
static int r_RV(struct SN_env * z);
static int r_mark_regions(struct SN_env * z);
static int r_postlude(struct SN_env * z);
static int r_prelude(struct SN_env * z);
#ifdef __cplusplus
extern "C" {
#endif


extern struct SN_env * portuguese_UTF_8_create_env(void);
extern void portuguese_UTF_8_close_env(struct SN_env * z);


#ifdef __cplusplus
}
#endif
static const symbol s_0_1[2] = { 0xC3, 0xA3 };
static const symbol s_0_2[2] = { 0xC3, 0xB5 };

static const struct among a_0[3] =
{
{ 0, 0, -1, 3, 0},
{ 2, s_0_1, 0, 1, 0},
{ 2, s_0_2, 0, 2, 0}
};

static const symbol s_1_1[2] = { 'a', '~' };
static const symbol s_1_2[2] = { 'o', '~' };

static const struct among a_1[3] =
{
{ 0, 0, -1, 3, 0},
{ 2, s_1_1, 0, 1, 0},
{ 2, s_1_2, 0, 2, 0}
};

static const symbol s_2_0[2] = { 'i', 'c' };
static const symbol s_2_1[2] = { 'a', 'd' };
static const symbol s_2_2[2] = { 'o', 's' };
static const symbol s_2_3[2] = { 'i', 'v' };

static const struct among a_2[4] =
{
{ 2, s_2_0, -1, -1, 0},
{ 2, s_2_1, -1, -1, 0},
{ 2, s_2_2, -1, -1, 0},
{ 2, s_2_3, -1, 1, 0}
};

static const symbol s_3_0[4] = { 'a', 'n', 't', 'e' };
static const symbol s_3_1[4] = { 'a', 'v', 'e', 'l' };
static const symbol s_3_2[5] = { 0xC3, 0xAD, 'v', 'e', 'l' };

static const struct among a_3[3] =
{
{ 4, s_3_0, -1, 1, 0},
{ 4, s_3_1, -1, 1, 0},
{ 5, s_3_2, -1, 1, 0}
};

static const symbol s_4_0[2] = { 'i', 'c' };
static const symbol s_4_1[4] = { 'a', 'b', 'i', 'l' };
static const symbol s_4_2[2] = { 'i', 'v' };

static const struct among a_4[3] =
{
{ 2, s_4_0, -1, 1, 0},
{ 4, s_4_1, -1, 1, 0},
{ 2, s_4_2, -1, 1, 0}
};

static const symbol s_5_0[3] = { 'i', 'c', 'a' };
static const symbol s_5_1[6] = { 0xC3, 0xA2, 'n', 'c', 'i', 'a' };
static const symbol s_5_2[6] = { 0xC3, 0xAA, 'n', 'c', 'i', 'a' };
static const symbol s_5_3[5] = { 'l', 'o', 'g', 'i', 'a' };
static const symbol s_5_4[3] = { 'i', 'r', 'a' };
static const symbol s_5_5[5] = { 'a', 'd', 'o', 'r', 'a' };
static const symbol s_5_6[3] = { 'o', 's', 'a' };
static const symbol s_5_7[4] = { 'i', 's', 't', 'a' };
static const symbol s_5_8[3] = { 'i', 'v', 'a' };
static const symbol s_5_9[3] = { 'e', 'z', 'a' };
static const symbol s_5_10[5] = { 'i', 'd', 'a', 'd', 'e' };
static const symbol s_5_11[4] = { 'a', 'n', 't', 'e' };
static const symbol s_5_12[5] = { 'm', 'e', 'n', 't', 'e' };
static const symbol s_5_13[6] = { 'a', 'm', 'e', 'n', 't', 'e' };
static const symbol s_5_14[5] = { 0xC3, 0xA1, 'v', 'e', 'l' };
static const symbol s_5_15[5] = { 0xC3, 0xAD, 'v', 'e', 'l' };
static const symbol s_5_16[3] = { 'i', 'c', 'o' };
static const symbol s_5_17[4] = { 'i', 's', 'm', 'o' };
static const symbol s_5_18[3] = { 'o', 's', 'o' };
static const symbol s_5_19[6] = { 'a', 'm', 'e', 'n', 't', 'o' };
static const symbol s_5_20[6] = { 'i', 'm', 'e', 'n', 't', 'o' };
static const symbol s_5_21[3] = { 'i', 'v', 'o' };
static const symbol s_5_22[6] = { 'a', 0xC3, 0xA7, 'a', '~', 'o' };
static const symbol s_5_23[6] = { 'u', 0xC3, 0xA7, 'a', '~', 'o' };
static const symbol s_5_24[4] = { 'a', 'd', 'o', 'r' };
static const symbol s_5_25[4] = { 'i', 'c', 'a', 's' };
static const symbol s_5_26[7] = { 0xC3, 0xAA, 'n', 'c', 'i', 'a', 's' };
static const symbol s_5_27[6] = { 'l', 'o', 'g', 'i', 'a', 's' };
static const symbol s_5_28[4] = { 'i', 'r', 'a', 's' };
static const symbol s_5_29[6] = { 'a', 'd', 'o', 'r', 'a', 's' };
static const symbol s_5_30[4] = { 'o', 's', 'a', 's' };
static const symbol s_5_31[5] = { 'i', 's', 't', 'a', 's' };
static const symbol s_5_32[4] = { 'i', 'v', 'a', 's' };
static const symbol s_5_33[4] = { 'e', 'z', 'a', 's' };
static const symbol s_5_34[6] = { 'i', 'd', 'a', 'd', 'e', 's' };
static const symbol s_5_35[6] = { 'a', 'd', 'o', 'r', 'e', 's' };
static const symbol s_5_36[5] = { 'a', 'n', 't', 'e', 's' };
static const symbol s_5_37[7] = { 'a', 0xC3, 0xA7, 'o', '~', 'e', 's' };
static const symbol s_5_38[7] = { 'u', 0xC3, 0xA7, 'o', '~', 'e', 's' };
static const symbol s_5_39[4] = { 'i', 'c', 'o', 's' };
static const symbol s_5_40[5] = { 'i', 's', 'm', 'o', 's' };
static const symbol s_5_41[4] = { 'o', 's', 'o', 's' };
static const symbol s_5_42[7] = { 'a', 'm', 'e', 'n', 't', 'o', 's' };
static const symbol s_5_43[7] = { 'i', 'm', 'e', 'n', 't', 'o', 's' };
static const symbol s_5_44[4] = { 'i', 'v', 'o', 's' };

static const struct among a_5[45] =
{
{ 3, s_5_0, -1, 1, 0},
{ 6, s_5_1, -1, 1, 0},
{ 6, s_5_2, -1, 4, 0},
{ 5, s_5_3, -1, 2, 0},
{ 3, s_5_4, -1, 9, 0},
{ 5, s_5_5, -1, 1, 0},
{ 3, s_5_6, -1, 1, 0},
{ 4, s_5_7, -1, 1, 0},
{ 3, s_5_8, -1, 8, 0},
{ 3, s_5_9, -1, 1, 0},
{ 5, s_5_10, -1, 7, 0},
{ 4, s_5_11, -1, 1, 0},
{ 5, s_5_12, -1, 6, 0},
{ 6, s_5_13, 12, 5, 0},
{ 5, s_5_14, -1, 1, 0},
{ 5, s_5_15, -1, 1, 0},
{ 3, s_5_16, -1, 1, 0},
{ 4, s_5_17, -1, 1, 0},
{ 3, s_5_18, -1, 1, 0},
{ 6, s_5_19, -1, 1, 0},
{ 6, s_5_20, -1, 1, 0},
{ 3, s_5_21, -1, 8, 0},
{ 6, s_5_22, -1, 1, 0},
{ 6, s_5_23, -1, 3, 0},
{ 4, s_5_24, -1, 1, 0},
{ 4, s_5_25, -1, 1, 0},
{ 7, s_5_26, -1, 4, 0},
{ 6, s_5_27, -1, 2, 0},
{ 4, s_5_28, -1, 9, 0},
{ 6, s_5_29, -1, 1, 0},
{ 4, s_5_30, -1, 1, 0},
{ 5, s_5_31, -1, 1, 0},
{ 4, s_5_32, -1, 8, 0},
{ 4, s_5_33, -1, 1, 0},
{ 6, s_5_34, -1, 7, 0},
{ 6, s_5_35, -1, 1, 0},
{ 5, s_5_36, -1, 1, 0},
{ 7, s_5_37, -1, 1, 0},
{ 7, s_5_38, -1, 3, 0},
{ 4, s_5_39, -1, 1, 0},
{ 5, s_5_40, -1, 1, 0},
{ 4, s_5_41, -1, 1, 0},
{ 7, s_5_42, -1, 1, 0},
{ 7, s_5_43, -1, 1, 0},
{ 4, s_5_44, -1, 8, 0}
};

static const symbol s_6_0[3] = { 'a', 'd', 'a' };
static const symbol s_6_1[3] = { 'i', 'd', 'a' };
static const symbol s_6_2[2] = { 'i', 'a' };
static const symbol s_6_3[4] = { 'a', 'r', 'i', 'a' };
static const symbol s_6_4[4] = { 'e', 'r', 'i', 'a' };
static const symbol s_6_5[4] = { 'i', 'r', 'i', 'a' };
static const symbol s_6_6[3] = { 'a', 'r', 'a' };
static const symbol s_6_7[3] = { 'e', 'r', 'a' };
static const symbol s_6_8[3] = { 'i', 'r', 'a' };
static const symbol s_6_9[3] = { 'a', 'v', 'a' };
static const symbol s_6_10[4] = { 'a', 's', 's', 'e' };
static const symbol s_6_11[4] = { 'e', 's', 's', 'e' };
static const symbol s_6_12[4] = { 'i', 's', 's', 'e' };
static const symbol s_6_13[4] = { 'a', 's', 't', 'e' };
static const symbol s_6_14[4] = { 'e', 's', 't', 'e' };
static const symbol s_6_15[4] = { 'i', 's', 't', 'e' };
static const symbol s_6_16[2] = { 'e', 'i' };
static const symbol s_6_17[4] = { 'a', 'r', 'e', 'i' };
static const symbol s_6_18[4] = { 'e', 'r', 'e', 'i' };
static const symbol s_6_19[4] = { 'i', 'r', 'e', 'i' };
static const symbol s_6_20[2] = { 'a', 'm' };
static const symbol s_6_21[3] = { 'i', 'a', 'm' };
static const symbol s_6_22[5] = { 'a', 'r', 'i', 'a', 'm' };
static const symbol s_6_23[5] = { 'e', 'r', 'i', 'a', 'm' };
static const symbol s_6_24[5] = { 'i', 'r', 'i', 'a', 'm' };
static const symbol s_6_25[4] = { 'a', 'r', 'a', 'm' };
static const symbol s_6_26[4] = { 'e', 'r', 'a', 'm' };
static const symbol s_6_27[4] = { 'i', 'r', 'a', 'm' };
static const symbol s_6_28[4] = { 'a', 'v', 'a', 'm' };
static const symbol s_6_29[2] = { 'e', 'm' };
static const symbol s_6_30[4] = { 'a', 'r', 'e', 'm' };
static const symbol s_6_31[4] = { 'e', 'r', 'e', 'm' };
static const symbol s_6_32[4] = { 'i', 'r', 'e', 'm' };
static const symbol s_6_33[5] = { 'a', 's', 's', 'e', 'm' };
static const symbol s_6_34[5] = { 'e', 's', 's', 'e', 'm' };
static const symbol s_6_35[5] = { 'i', 's', 's', 'e', 'm' };
static const symbol s_6_36[3] = { 'a', 'd', 'o' };
static const symbol s_6_37[3] = { 'i', 'd', 'o' };
static const symbol s_6_38[4] = { 'a', 'n', 'd', 'o' };
static const symbol s_6_39[4] = { 'e', 'n', 'd', 'o' };
static const symbol s_6_40[4] = { 'i', 'n', 'd', 'o' };
static const symbol s_6_41[5] = { 'a', 'r', 'a', '~', 'o' };
static const symbol s_6_42[5] = { 'e', 'r', 'a', '~', 'o' };
static const symbol s_6_43[5] = { 'i', 'r', 'a', '~', 'o' };
static const symbol s_6_44[2] = { 'a', 'r' };
static const symbol s_6_45[2] = { 'e', 'r' };
static const symbol s_6_46[2] = { 'i', 'r' };
static const symbol s_6_47[2] = { 'a', 's' };
static const symbol s_6_48[4] = { 'a', 'd', 'a', 's' };
static const symbol s_6_49[4] = { 'i', 'd', 'a', 's' };
static const symbol s_6_50[3] = { 'i', 'a', 's' };
static const symbol s_6_51[5] = { 'a', 'r', 'i', 'a', 's' };
static const symbol s_6_52[5] = { 'e', 'r', 'i', 'a', 's' };
static const symbol s_6_53[5] = { 'i', 'r', 'i', 'a', 's' };
static const symbol s_6_54[4] = { 'a', 'r', 'a', 's' };
static const symbol s_6_55[4] = { 'e', 'r', 'a', 's' };
static const symbol s_6_56[4] = { 'i', 'r', 'a', 's' };
static const symbol s_6_57[4] = { 'a', 'v', 'a', 's' };
static const symbol s_6_58[2] = { 'e', 's' };
static const symbol s_6_59[5] = { 'a', 'r', 'd', 'e', 's' };
static const symbol s_6_60[5] = { 'e', 'r', 'd', 'e', 's' };
static const symbol s_6_61[5] = { 'i', 'r', 'd', 'e', 's' };
static const symbol s_6_62[4] = { 'a', 'r', 'e', 's' };
static const symbol s_6_63[4] = { 'e', 'r', 'e', 's' };
static const symbol s_6_64[4] = { 'i', 'r', 'e', 's' };
static const symbol s_6_65[5] = { 'a', 's', 's', 'e', 's' };
static const symbol s_6_66[5] = { 'e', 's', 's', 'e', 's' };
static const symbol s_6_67[5] = { 'i', 's', 's', 'e', 's' };
static const symbol s_6_68[5] = { 'a', 's', 't', 'e', 's' };
static const symbol s_6_69[5] = { 'e', 's', 't', 'e', 's' };
static const symbol s_6_70[5] = { 'i', 's', 't', 'e', 's' };
static const symbol s_6_71[2] = { 'i', 's' };
static const symbol s_6_72[3] = { 'a', 'i', 's' };
static const symbol s_6_73[3] = { 'e', 'i', 's' };
static const symbol s_6_74[5] = { 'a', 'r', 'e', 'i', 's' };
static const symbol s_6_75[5] = { 'e', 'r', 'e', 'i', 's' };
static const symbol s_6_76[5] = { 'i', 'r', 'e', 'i', 's' };
static const symbol s_6_77[6] = { 0xC3, 0xA1, 'r', 'e', 'i', 's' };
static const symbol s_6_78[6] = { 0xC3, 0xA9, 'r', 'e', 'i', 's' };
static const symbol s_6_79[6] = { 0xC3, 0xAD, 'r', 'e', 'i', 's' };
static const symbol s_6_80[7] = { 0xC3, 0xA1, 's', 's', 'e', 'i', 's' };
static const symbol s_6_81[7] = { 0xC3, 0xA9, 's', 's', 'e', 'i', 's' };
static const symbol s_6_82[7] = { 0xC3, 0xAD, 's', 's', 'e', 'i', 's' };
static const symbol s_6_83[6] = { 0xC3, 0xA1, 'v', 'e', 'i', 's' };
static const symbol s_6_84[5] = { 0xC3, 0xAD, 'e', 'i', 's' };
static const symbol s_6_85[7] = { 'a', 'r', 0xC3, 0xAD, 'e', 'i', 's' };
static const symbol s_6_86[7] = { 'e', 'r', 0xC3, 0xAD, 'e', 'i', 's' };
static const symbol s_6_87[7] = { 'i', 'r', 0xC3, 0xAD, 'e', 'i', 's' };
static const symbol s_6_88[4] = { 'a', 'd', 'o', 's' };
static const symbol s_6_89[4] = { 'i', 'd', 'o', 's' };
static const symbol s_6_90[4] = { 'a', 'm', 'o', 's' };
static const symbol s_6_91[7] = { 0xC3, 0xA1, 'r', 'a', 'm', 'o', 's' };
static const symbol s_6_92[7] = { 0xC3, 0xA9, 'r', 'a', 'm', 'o', 's' };
static const symbol s_6_93[7] = { 0xC3, 0xAD, 'r', 'a', 'm', 'o', 's' };
static const symbol s_6_94[7] = { 0xC3, 0xA1, 'v', 'a', 'm', 'o', 's' };
static const symbol s_6_95[6] = { 0xC3, 0xAD, 'a', 'm', 'o', 's' };
static const symbol s_6_96[8] = { 'a', 'r', 0xC3, 0xAD, 'a', 'm', 'o', 's' };
static const symbol s_6_97[8] = { 'e', 'r', 0xC3, 0xAD, 'a', 'm', 'o', 's' };
static const symbol s_6_98[8] = { 'i', 'r', 0xC3, 0xAD, 'a', 'm', 'o', 's' };
static const symbol s_6_99[4] = { 'e', 'm', 'o', 's' };
static const symbol s_6_100[6] = { 'a', 'r', 'e', 'm', 'o', 's' };
static const symbol s_6_101[6] = { 'e', 'r', 'e', 'm', 'o', 's' };
static const symbol s_6_102[6] = { 'i', 'r', 'e', 'm', 'o', 's' };
static const symbol s_6_103[8] = { 0xC3, 0xA1, 's', 's', 'e', 'm', 'o', 's' };
static const symbol s_6_104[8] = { 0xC3, 0xAA, 's', 's', 'e', 'm', 'o', 's' };
static const symbol s_6_105[8] = { 0xC3, 0xAD, 's', 's', 'e', 'm', 'o', 's' };
static const symbol s_6_106[4] = { 'i', 'm', 'o', 's' };
static const symbol s_6_107[5] = { 'a', 'r', 'm', 'o', 's' };
static const symbol s_6_108[5] = { 'e', 'r', 'm', 'o', 's' };
static const symbol s_6_109[5] = { 'i', 'r', 'm', 'o', 's' };
static const symbol s_6_110[5] = { 0xC3, 0xA1, 'm', 'o', 's' };
static const symbol s_6_111[5] = { 'a', 'r', 0xC3, 0xA1, 's' };
static const symbol s_6_112[5] = { 'e', 'r', 0xC3, 0xA1, 's' };
static const symbol s_6_113[5] = { 'i', 'r', 0xC3, 0xA1, 's' };
static const symbol s_6_114[2] = { 'e', 'u' };
static const symbol s_6_115[2] = { 'i', 'u' };
static const symbol s_6_116[2] = { 'o', 'u' };
static const symbol s_6_117[4] = { 'a', 'r', 0xC3, 0xA1 };
static const symbol s_6_118[4] = { 'e', 'r', 0xC3, 0xA1 };
static const symbol s_6_119[4] = { 'i', 'r', 0xC3, 0xA1 };

static const struct among a_6[120] =
{
{ 3, s_6_0, -1, 1, 0},
{ 3, s_6_1, -1, 1, 0},
{ 2, s_6_2, -1, 1, 0},
{ 4, s_6_3, 2, 1, 0},
{ 4, s_6_4, 2, 1, 0},
{ 4, s_6_5, 2, 1, 0},
{ 3, s_6_6, -1, 1, 0},
{ 3, s_6_7, -1, 1, 0},
{ 3, s_6_8, -1, 1, 0},
{ 3, s_6_9, -1, 1, 0},
{ 4, s_6_10, -1, 1, 0},
{ 4, s_6_11, -1, 1, 0},
{ 4, s_6_12, -1, 1, 0},
{ 4, s_6_13, -1, 1, 0},
{ 4, s_6_14, -1, 1, 0},
{ 4, s_6_15, -1, 1, 0},
{ 2, s_6_16, -1, 1, 0},
{ 4, s_6_17, 16, 1, 0},
{ 4, s_6_18, 16, 1, 0},
{ 4, s_6_19, 16, 1, 0},
{ 2, s_6_20, -1, 1, 0},
{ 3, s_6_21, 20, 1, 0},
{ 5, s_6_22, 21, 1, 0},
{ 5, s_6_23, 21, 1, 0},
{ 5, s_6_24, 21, 1, 0},
{ 4, s_6_25, 20, 1, 0},
{ 4, s_6_26, 20, 1, 0},
{ 4, s_6_27, 20, 1, 0},
{ 4, s_6_28, 20, 1, 0},
{ 2, s_6_29, -1, 1, 0},
{ 4, s_6_30, 29, 1, 0},
{ 4, s_6_31, 29, 1, 0},
{ 4, s_6_32, 29, 1, 0},
{ 5, s_6_33, 29, 1, 0},
{ 5, s_6_34, 29, 1, 0},
{ 5, s_6_35, 29, 1, 0},
{ 3, s_6_36, -1, 1, 0},
{ 3, s_6_37, -1, 1, 0},
{ 4, s_6_38, -1, 1, 0},
{ 4, s_6_39, -1, 1, 0},
{ 4, s_6_40, -1, 1, 0},
{ 5, s_6_41, -1, 1, 0},
{ 5, s_6_42, -1, 1, 0},
{ 5, s_6_43, -1, 1, 0},
{ 2, s_6_44, -1, 1, 0},
{ 2, s_6_45, -1, 1, 0},
{ 2, s_6_46, -1, 1, 0},
{ 2, s_6_47, -1, 1, 0},
{ 4, s_6_48, 47, 1, 0},
{ 4, s_6_49, 47, 1, 0},
{ 3, s_6_50, 47, 1, 0},
{ 5, s_6_51, 50, 1, 0},
{ 5, s_6_52, 50, 1, 0},
{ 5, s_6_53, 50, 1, 0},
{ 4, s_6_54, 47, 1, 0},
{ 4, s_6_55, 47, 1, 0},
{ 4, s_6_56, 47, 1, 0},
{ 4, s_6_57, 47, 1, 0},
{ 2, s_6_58, -1, 1, 0},
{ 5, s_6_59, 58, 1, 0},
{ 5, s_6_60, 58, 1, 0},
{ 5, s_6_61, 58, 1, 0},
{ 4, s_6_62, 58, 1, 0},
{ 4, s_6_63, 58, 1, 0},
{ 4, s_6_64, 58, 1, 0},
{ 5, s_6_65, 58, 1, 0},
{ 5, s_6_66, 58, 1, 0},
{ 5, s_6_67, 58, 1, 0},
{ 5, s_6_68, 58, 1, 0},
{ 5, s_6_69, 58, 1, 0},
{ 5, s_6_70, 58, 1, 0},
{ 2, s_6_71, -1, 1, 0},
{ 3, s_6_72, 71, 1, 0},
{ 3, s_6_73, 71, 1, 0},
{ 5, s_6_74, 73, 1, 0},
{ 5, s_6_75, 73, 1, 0},
{ 5, s_6_76, 73, 1, 0},
{ 6, s_6_77, 73, 1, 0},
{ 6, s_6_78, 73, 1, 0},
{ 6, s_6_79, 73, 1, 0},
{ 7, s_6_80, 73, 1, 0},
{ 7, s_6_81, 73, 1, 0},
{ 7, s_6_82, 73, 1, 0},
{ 6, s_6_83, 73, 1, 0},
{ 5, s_6_84, 73, 1, 0},
{ 7, s_6_85, 84, 1, 0},
{ 7, s_6_86, 84, 1, 0},
{ 7, s_6_87, 84, 1, 0},
{ 4, s_6_88, -1, 1, 0},
{ 4, s_6_89, -1, 1, 0},
{ 4, s_6_90, -1, 1, 0},
{ 7, s_6_91, 90, 1, 0},
{ 7, s_6_92, 90, 1, 0},
{ 7, s_6_93, 90, 1, 0},
{ 7, s_6_94, 90, 1, 0},
{ 6, s_6_95, 90, 1, 0},
{ 8, s_6_96, 95, 1, 0},
{ 8, s_6_97, 95, 1, 0},
{ 8, s_6_98, 95, 1, 0},
{ 4, s_6_99, -1, 1, 0},
{ 6, s_6_100, 99, 1, 0},
{ 6, s_6_101, 99, 1, 0},
{ 6, s_6_102, 99, 1, 0},
{ 8, s_6_103, 99, 1, 0},
{ 8, s_6_104, 99, 1, 0},
{ 8, s_6_105, 99, 1, 0},
{ 4, s_6_106, -1, 1, 0},
{ 5, s_6_107, -1, 1, 0},
{ 5, s_6_108, -1, 1, 0},
{ 5, s_6_109, -1, 1, 0},
{ 5, s_6_110, -1, 1, 0},
{ 5, s_6_111, -1, 1, 0},
{ 5, s_6_112, -1, 1, 0},
{ 5, s_6_113, -1, 1, 0},
{ 2, s_6_114, -1, 1, 0},
{ 2, s_6_115, -1, 1, 0},
{ 2, s_6_116, -1, 1, 0},
{ 4, s_6_117, -1, 1, 0},
{ 4, s_6_118, -1, 1, 0},
{ 4, s_6_119, -1, 1, 0}
};

static const symbol s_7_0[1] = { 'a' };
static const symbol s_7_1[1] = { 'i' };
static const symbol s_7_2[1] = { 'o' };
static const symbol s_7_3[2] = { 'o', 's' };
static const symbol s_7_4[2] = { 0xC3, 0xA1 };
static const symbol s_7_5[2] = { 0xC3, 0xAD };
static const symbol s_7_6[2] = { 0xC3, 0xB3 };

static const struct among a_7[7] =
{
{ 1, s_7_0, -1, 1, 0},
{ 1, s_7_1, -1, 1, 0},
{ 1, s_7_2, -1, 1, 0},
{ 2, s_7_3, -1, 1, 0},
{ 2, s_7_4, -1, 1, 0},
{ 2, s_7_5, -1, 1, 0},
{ 2, s_7_6, -1, 1, 0}
};

static const symbol s_8_0[1] = { 'e' };
static const symbol s_8_1[2] = { 0xC3, 0xA7 };
static const symbol s_8_2[2] = { 0xC3, 0xA9 };
static const symbol s_8_3[2] = { 0xC3, 0xAA };

static const struct among a_8[4] =
{
{ 1, s_8_0, -1, 1, 0},
{ 2, s_8_1, -1, 2, 0},
{ 2, s_8_2, -1, 1, 0},
{ 2, s_8_3, -1, 1, 0}
};

static const unsigned char g_v[] = { 17, 65, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 19, 12, 2 };

static const symbol s_0[] = { 'a', '~' };
static const symbol s_1[] = { 'o', '~' };
static const symbol s_2[] = { 0xC3, 0xA3 };
static const symbol s_3[] = { 0xC3, 0xB5 };
static const symbol s_4[] = { 'l', 'o', 'g' };
static const symbol s_5[] = { 'u' };
static const symbol s_6[] = { 'e', 'n', 't', 'e' };
static const symbol s_7[] = { 'a', 't' };
static const symbol s_8[] = { 'a', 't' };
static const symbol s_9[] = { 'i', 'r' };
static const symbol s_10[] = { 'c' };

static int r_prelude(struct SN_env * z) {
    int among_var;
    while(1) {
        int c1 = z->c;
        z->bra = z->c;
        if (z->c + 1 >= z->l || (z->p[z->c + 1] != 163 && z->p[z->c + 1] != 181)) among_var = 3; else
        among_var = find_among(z, a_0, 3);
        if (!(among_var)) goto lab0;
        z->ket = z->c;
        switch (among_var) {
            case 1:
                {   int ret = slice_from_s(z, 2, s_0);
                    if (ret < 0) return ret;
                }
                break;
            case 2:
                {   int ret = slice_from_s(z, 2, s_1);
                    if (ret < 0) return ret;
                }
                break;
            case 3:
                {   int ret = skip_utf8(z->p, z->c, 0, z->l, 1);
                    if (ret < 0) goto lab0;
                    z->c = ret;
                }
                break;
        }
        continue;
    lab0:
        z->c = c1;
        break;
    }
    return 1;
}

static int r_mark_regions(struct SN_env * z) {
    z->I[2] = z->l;
    z->I[1] = z->l;
    z->I[0] = z->l;
    {   int c1 = z->c;
        {   int c2 = z->c;
            if (in_grouping_U(z, g_v, 97, 250, 0)) goto lab2;
            {   int c3 = z->c;
                if (out_grouping_U(z, g_v, 97, 250, 0)) goto lab4;
                {   
                    int ret = out_grouping_U(z, g_v, 97, 250, 1);
                    if (ret < 0) goto lab4;
                    z->c += ret;
                }
                goto lab3;
            lab4:
                z->c = c3;
                if (in_grouping_U(z, g_v, 97, 250, 0)) goto lab2;
                {   
                    int ret = in_grouping_U(z, g_v, 97, 250, 1);
                    if (ret < 0) goto lab2;
                    z->c += ret;
                }
            }
        lab3:
            goto lab1;
        lab2:
            z->c = c2;
            if (out_grouping_U(z, g_v, 97, 250, 0)) goto lab0;
            {   int c4 = z->c;
                if (out_grouping_U(z, g_v, 97, 250, 0)) goto lab6;
                {   
                    int ret = out_grouping_U(z, g_v, 97, 250, 1);
                    if (ret < 0) goto lab6;
                    z->c += ret;
                }
                goto lab5;
            lab6:
                z->c = c4;
                if (in_grouping_U(z, g_v, 97, 250, 0)) goto lab0;
                {   int ret = skip_utf8(z->p, z->c, 0, z->l, 1);
                    if (ret < 0) goto lab0;
                    z->c = ret;
                }
            }
        lab5:
            ;
        }
    lab1:
        z->I[2] = z->c;
    lab0:
        z->c = c1;
    }
    {   int c5 = z->c;
        {   
            int ret = out_grouping_U(z, g_v, 97, 250, 1);
            if (ret < 0) goto lab7;
            z->c += ret;
        }
        {   
            int ret = in_grouping_U(z, g_v, 97, 250, 1);
            if (ret < 0) goto lab7;
            z->c += ret;
        }
        z->I[1] = z->c;
        {   
            int ret = out_grouping_U(z, g_v, 97, 250, 1);
            if (ret < 0) goto lab7;
            z->c += ret;
        }
        {   
            int ret = in_grouping_U(z, g_v, 97, 250, 1);
            if (ret < 0) goto lab7;
            z->c += ret;
        }
        z->I[0] = z->c;
    lab7:
        z->c = c5;
    }
    return 1;
}

static int r_postlude(struct SN_env * z) {
    int among_var;
    while(1) {
        int c1 = z->c;
        z->bra = z->c;
        if (z->c + 1 >= z->l || z->p[z->c + 1] != 126) among_var = 3; else
        among_var = find_among(z, a_1, 3);
        if (!(among_var)) goto lab0;
        z->ket = z->c;
        switch (among_var) {
            case 1:
                {   int ret = slice_from_s(z, 2, s_2);
                    if (ret < 0) return ret;
                }
                break;
            case 2:
                {   int ret = slice_from_s(z, 2, s_3);
                    if (ret < 0) return ret;
                }
                break;
            case 3:
                {   int ret = skip_utf8(z->p, z->c, 0, z->l, 1);
                    if (ret < 0) goto lab0;
                    z->c = ret;
                }
                break;
        }
        continue;
    lab0:
        z->c = c1;
        break;
    }
    return 1;
}

static int r_RV(struct SN_env * z) {
    if (!(z->I[2] <= z->c)) return 0;
    return 1;
}

static int r_R1(struct SN_env * z) {
    if (!(z->I[1] <= z->c)) return 0;
    return 1;
}

static int r_R2(struct SN_env * z) {
    if (!(z->I[0] <= z->c)) return 0;
    return 1;
}

static int r_standard_suffix(struct SN_env * z) {
    int among_var;
    z->ket = z->c;
    if (z->c - 2 <= z->lb || z->p[z->c - 1] >> 5 != 3 || !((823330 >> (z->p[z->c - 1] & 0x1f)) & 1)) return 0;
    among_var = find_among_b(z, a_5, 45);
    if (!(among_var)) return 0;
    z->bra = z->c;
    switch (among_var) {
        case 1:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            break;
        case 2:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_from_s(z, 3, s_4);
                if (ret < 0) return ret;
            }
            break;
        case 3:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_from_s(z, 1, s_5);
                if (ret < 0) return ret;
            }
            break;
        case 4:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_from_s(z, 4, s_6);
                if (ret < 0) return ret;
            }
            break;
        case 5:
            {   int ret = r_R1(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            {   int m1 = z->l - z->c; (void)m1;
                z->ket = z->c;
                if (z->c - 1 <= z->lb || z->p[z->c - 1] >> 5 != 3 || !((4718616 >> (z->p[z->c - 1] & 0x1f)) & 1)) { z->c = z->l - m1; goto lab0; }
                among_var = find_among_b(z, a_2, 4);
                if (!(among_var)) { z->c = z->l - m1; goto lab0; }
                z->bra = z->c;
                {   int ret = r_R2(z);
                    if (ret == 0) { z->c = z->l - m1; goto lab0; }
                    if (ret < 0) return ret;
                }
                {   int ret = slice_del(z);
                    if (ret < 0) return ret;
                }
                switch (among_var) {
                    case 1:
                        z->ket = z->c;
                        if (!(eq_s_b(z, 2, s_7))) { z->c = z->l - m1; goto lab0; }
                        z->bra = z->c;
                        {   int ret = r_R2(z);
                            if (ret == 0) { z->c = z->l - m1; goto lab0; }
                            if (ret < 0) return ret;
                        }
                        {   int ret = slice_del(z);
                            if (ret < 0) return ret;
                        }
                        break;
                }
            lab0:
                ;
            }
            break;
        case 6:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            {   int m2 = z->l - z->c; (void)m2;
                z->ket = z->c;
                if (z->c - 3 <= z->lb || (z->p[z->c - 1] != 101 && z->p[z->c - 1] != 108)) { z->c = z->l - m2; goto lab1; }
                if (!(find_among_b(z, a_3, 3))) { z->c = z->l - m2; goto lab1; }
                z->bra = z->c;
                {   int ret = r_R2(z);
                    if (ret == 0) { z->c = z->l - m2; goto lab1; }
                    if (ret < 0) return ret;
                }
                {   int ret = slice_del(z);
                    if (ret < 0) return ret;
                }
            lab1:
                ;
            }
            break;
        case 7:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            {   int m3 = z->l - z->c; (void)m3;
                z->ket = z->c;
                if (z->c - 1 <= z->lb || z->p[z->c - 1] >> 5 != 3 || !((4198408 >> (z->p[z->c - 1] & 0x1f)) & 1)) { z->c = z->l - m3; goto lab2; }
                if (!(find_among_b(z, a_4, 3))) { z->c = z->l - m3; goto lab2; }
                z->bra = z->c;
                {   int ret = r_R2(z);
                    if (ret == 0) { z->c = z->l - m3; goto lab2; }
                    if (ret < 0) return ret;
                }
                {   int ret = slice_del(z);
                    if (ret < 0) return ret;
                }
            lab2:
                ;
            }
            break;
        case 8:
            {   int ret = r_R2(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            {   int m4 = z->l - z->c; (void)m4;
                z->ket = z->c;
                if (!(eq_s_b(z, 2, s_8))) { z->c = z->l - m4; goto lab3; }
                z->bra = z->c;
                {   int ret = r_R2(z);
                    if (ret == 0) { z->c = z->l - m4; goto lab3; }
                    if (ret < 0) return ret;
                }
                {   int ret = slice_del(z);
                    if (ret < 0) return ret;
                }
            lab3:
                ;
            }
            break;
        case 9:
            {   int ret = r_RV(z);
                if (ret <= 0) return ret;
            }
            if (z->c <= z->lb || z->p[z->c - 1] != 'e') return 0;
            z->c--;
            {   int ret = slice_from_s(z, 2, s_9);
                if (ret < 0) return ret;
            }
            break;
    }
    return 1;
}

static int r_verb_suffix(struct SN_env * z) {

    {   int mlimit1;
        if (z->c < z->I[2]) return 0;
        mlimit1 = z->lb; z->lb = z->I[2];
        z->ket = z->c;
        if (!(find_among_b(z, a_6, 120))) { z->lb = mlimit1; return 0; }
        z->bra = z->c;
        {   int ret = slice_del(z);
            if (ret < 0) return ret;
        }
        z->lb = mlimit1;
    }
    return 1;
}

static int r_residual_suffix(struct SN_env * z) {
    z->ket = z->c;
    if (!(find_among_b(z, a_7, 7))) return 0;
    z->bra = z->c;
    {   int ret = r_RV(z);
        if (ret <= 0) return ret;
    }
    {   int ret = slice_del(z);
        if (ret < 0) return ret;
    }
    return 1;
}

static int r_residual_form(struct SN_env * z) {
    int among_var;
    z->ket = z->c;
    among_var = find_among_b(z, a_8, 4);
    if (!(among_var)) return 0;
    z->bra = z->c;
    switch (among_var) {
        case 1:
            {   int ret = r_RV(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            z->ket = z->c;
            {   int m1 = z->l - z->c; (void)m1;
                if (z->c <= z->lb || z->p[z->c - 1] != 'u') goto lab1;
                z->c--;
                z->bra = z->c;
                {   int m_test2 = z->l - z->c;
                    if (z->c <= z->lb || z->p[z->c - 1] != 'g') goto lab1;
                    z->c--;
                    z->c = z->l - m_test2;
                }
                goto lab0;
            lab1:
                z->c = z->l - m1;
                if (z->c <= z->lb || z->p[z->c - 1] != 'i') return 0;
                z->c--;
                z->bra = z->c;
                {   int m_test3 = z->l - z->c;
                    if (z->c <= z->lb || z->p[z->c - 1] != 'c') return 0;
                    z->c--;
                    z->c = z->l - m_test3;
                }
            }
        lab0:
            {   int ret = r_RV(z);
                if (ret <= 0) return ret;
            }
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            break;
        case 2:
            {   int ret = slice_from_s(z, 1, s_10);
                if (ret < 0) return ret;
            }
            break;
    }
    return 1;
}

extern int portuguese_UTF_8_stem(struct SN_env * z) {
    {   int c1 = z->c;
        {   int ret = r_prelude(z);
            if (ret < 0) return ret;
        }
        z->c = c1;
    }
    
    {   int ret = r_mark_regions(z);
        if (ret < 0) return ret;
    }
    z->lb = z->c; z->c = z->l;

    {   int m2 = z->l - z->c; (void)m2;
        {   int m3 = z->l - z->c; (void)m3;
            {   int m4 = z->l - z->c; (void)m4;
                {   int m5 = z->l - z->c; (void)m5;
                    {   int ret = r_standard_suffix(z);
                        if (ret == 0) goto lab4;
                        if (ret < 0) return ret;
                    }
                    goto lab3;
                lab4:
                    z->c = z->l - m5;
                    {   int ret = r_verb_suffix(z);
                        if (ret == 0) goto lab2;
                        if (ret < 0) return ret;
                    }
                }
            lab3:
                z->c = z->l - m4;
                {   int m6 = z->l - z->c; (void)m6;
                    z->ket = z->c;
                    if (z->c <= z->lb || z->p[z->c - 1] != 'i') goto lab5;
                    z->c--;
                    z->bra = z->c;
                    {   int m_test7 = z->l - z->c;
                        if (z->c <= z->lb || z->p[z->c - 1] != 'c') goto lab5;
                        z->c--;
                        z->c = z->l - m_test7;
                    }
                    {   int ret = r_RV(z);
                        if (ret == 0) goto lab5;
                        if (ret < 0) return ret;
                    }
                    {   int ret = slice_del(z);
                        if (ret < 0) return ret;
                    }
                lab5:
                    z->c = z->l - m6;
                }
            }
            goto lab1;
        lab2:
            z->c = z->l - m3;
            {   int ret = r_residual_suffix(z);
                if (ret == 0) goto lab0;
                if (ret < 0) return ret;
            }
        }
    lab1:
    lab0:
        z->c = z->l - m2;
    }
    {   int m8 = z->l - z->c; (void)m8;
        {   int ret = r_residual_form(z);
            if (ret < 0) return ret;
        }
        z->c = z->l - m8;
    }
    z->c = z->lb;
    {   int c9 = z->c;
        {   int ret = r_postlude(z);
            if (ret < 0) return ret;
        }
        z->c = c9;
    }
    return 1;
}

extern struct SN_env * portuguese_UTF_8_create_env(void) { return SN_create_env(0, 3); }

extern void portuguese_UTF_8_close_env(struct SN_env * z) { SN_close_env(z, 0); }

