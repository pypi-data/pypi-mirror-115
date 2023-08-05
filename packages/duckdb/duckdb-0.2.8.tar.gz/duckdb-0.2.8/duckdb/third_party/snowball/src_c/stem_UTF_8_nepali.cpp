/* Generated by Snowball 2.0.0 - https://snowballstem.org/ */

#include "../runtime/header.h"

#ifdef __cplusplus
extern "C" {
#endif
extern int nepali_UTF_8_stem(struct SN_env * z);
#ifdef __cplusplus
}
#endif
static int r_remove_category_3(struct SN_env * z);
static int r_remove_category_2(struct SN_env * z);
static int r_check_category_2(struct SN_env * z);
static int r_remove_category_1(struct SN_env * z);
#ifdef __cplusplus
extern "C" {
#endif


extern struct SN_env * nepali_UTF_8_create_env(void);
extern void nepali_UTF_8_close_env(struct SN_env * z);


#ifdef __cplusplus
}
#endif
static const symbol s_0_0[6] = { 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x80 };
static const symbol s_0_1[9] = { 0xE0, 0xA4, 0xB2, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0x87 };
static const symbol s_0_2[6] = { 0xE0, 0xA4, 0xB2, 0xE0, 0xA5, 0x87 };
static const symbol s_0_3[9] = { 0xE0, 0xA4, 0xB2, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0x88 };
static const symbol s_0_4[6] = { 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x88 };
static const symbol s_0_5[12] = { 0xE0, 0xA4, 0xB8, 0xE0, 0xA4, 0x81, 0xE0, 0xA4, 0x97, 0xE0, 0xA5, 0x88 };
static const symbol s_0_6[6] = { 0xE0, 0xA4, 0xAE, 0xE0, 0xA5, 0x88 };
static const symbol s_0_7[6] = { 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_0_8[9] = { 0xE0, 0xA4, 0xB8, 0xE0, 0xA4, 0x81, 0xE0, 0xA4, 0x97 };
static const symbol s_0_9[9] = { 0xE0, 0xA4, 0xB8, 0xE0, 0xA4, 0x82, 0xE0, 0xA4, 0x97 };
static const symbol s_0_10[18] = { 0xE0, 0xA4, 0xAE, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0xB0, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xAB, 0xE0, 0xA4, 0xA4 };
static const symbol s_0_11[6] = { 0xE0, 0xA4, 0xB0, 0xE0, 0xA4, 0xA4 };
static const symbol s_0_12[6] = { 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_0_13[6] = { 0xE0, 0xA4, 0xAE, 0xE0, 0xA4, 0xBE };
static const symbol s_0_14[18] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xB5, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0xB0, 0xE0, 0xA4, 0xBE };
static const symbol s_0_15[6] = { 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBF };
static const symbol s_0_16[9] = { 0xE0, 0xA4, 0xAA, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xBF };

static const struct among a_0[17] =
{
{ 6, s_0_0, -1, 2, 0},
{ 9, s_0_1, -1, 1, 0},
{ 6, s_0_2, -1, 1, 0},
{ 9, s_0_3, -1, 1, 0},
{ 6, s_0_4, -1, 2, 0},
{ 12, s_0_5, -1, 1, 0},
{ 6, s_0_6, -1, 1, 0},
{ 6, s_0_7, -1, 2, 0},
{ 9, s_0_8, -1, 1, 0},
{ 9, s_0_9, -1, 1, 0},
{ 18, s_0_10, -1, 1, 0},
{ 6, s_0_11, -1, 1, 0},
{ 6, s_0_12, -1, 2, 0},
{ 6, s_0_13, -1, 1, 0},
{ 18, s_0_14, -1, 1, 0},
{ 6, s_0_15, -1, 2, 0},
{ 9, s_0_16, -1, 1, 0}
};

static const symbol s_1_0[3] = { 0xE0, 0xA4, 0x81 };
static const symbol s_1_1[3] = { 0xE0, 0xA4, 0x82 };
static const symbol s_1_2[3] = { 0xE0, 0xA5, 0x88 };

static const struct among a_1[3] =
{
{ 3, s_1_0, -1, -1, 0},
{ 3, s_1_1, -1, -1, 0},
{ 3, s_1_2, -1, -1, 0}
};

static const symbol s_2_0[3] = { 0xE0, 0xA4, 0x81 };
static const symbol s_2_1[3] = { 0xE0, 0xA4, 0x82 };
static const symbol s_2_2[3] = { 0xE0, 0xA5, 0x88 };

static const struct among a_2[3] =
{
{ 3, s_2_0, -1, 1, 0},
{ 3, s_2_1, -1, 1, 0},
{ 3, s_2_2, -1, 2, 0}
};

static const symbol s_3_0[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x80 };
static const symbol s_3_1[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x80 };
static const symbol s_3_2[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x80 };
static const symbol s_3_3[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x80 };
static const symbol s_3_4[12] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x96, 0xE0, 0xA5, 0x80 };
static const symbol s_3_5[6] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA5, 0x80 };
static const symbol s_3_6[6] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x80 };
static const symbol s_3_7[6] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x81 };
static const symbol s_3_8[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x81 };
static const symbol s_3_9[12] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x81 };
static const symbol s_3_10[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x81 };
static const symbol s_3_11[6] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x81 };
static const symbol s_3_12[9] = { 0xE0, 0xA4, 0xB9, 0xE0, 0xA4, 0xB0, 0xE0, 0xA5, 0x81 };
static const symbol s_3_13[9] = { 0xE0, 0xA4, 0xB9, 0xE0, 0xA4, 0xB0, 0xE0, 0xA5, 0x82 };
static const symbol s_3_14[6] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x87 };
static const symbol s_3_15[6] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA5, 0x87 };
static const symbol s_3_16[6] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87 };
static const symbol s_3_17[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x88 };
static const symbol s_3_18[12] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x88 };
static const symbol s_3_19[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x88 };
static const symbol s_3_20[6] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x88 };
static const symbol s_3_21[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x88 };
static const symbol s_3_22[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x88 };
static const symbol s_3_23[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_3_24[12] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_3_25[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_3_26[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_3_27[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA5, 0x8B };
static const symbol s_3_28[6] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x8B };
static const symbol s_3_29[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x8B };
static const symbol s_3_30[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x8B };
static const symbol s_3_31[6] = { 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_32[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_33[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_34[9] = { 0xE0, 0xA4, 0xAD, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_35[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_36[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_37[12] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8B };
static const symbol s_3_38[6] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_39[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_40[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_41[12] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_42[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_43[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_3_44[6] = { 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8C };
static const symbol s_3_45[12] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8C };
static const symbol s_3_46[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8C };
static const symbol s_3_47[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8C };
static const symbol s_3_48[9] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_49[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_50[12] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_51[15] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_52[12] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_53[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_54[12] = { 0xE0, 0xA4, 0xB2, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_55[12] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_56[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_57[9] = { 0xE0, 0xA4, 0xAA, 0xE0, 0xA4, 0xB0, 0xE0, 0xA5, 0x8D };
static const symbol s_3_58[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_59[15] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_60[12] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_61[12] = { 0xE0, 0xA4, 0xB9, 0xE0, 0xA5, 0x8B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_62[9] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_63[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_64[12] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_65[15] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_66[12] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_67[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x9B, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_68[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_69[12] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xB8, 0xE0, 0xA5, 0x8D };
static const symbol s_3_70[9] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x8F };
static const symbol s_3_71[3] = { 0xE0, 0xA4, 0x9B };
static const symbol s_3_72[6] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x9B };
static const symbol s_3_73[6] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B };
static const symbol s_3_74[9] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B };
static const symbol s_3_75[15] = { 0xE0, 0xA4, 0xB9, 0xE0, 0xA5, 0x81, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x9B };
static const symbol s_3_76[15] = { 0xE0, 0xA4, 0xB9, 0xE0, 0xA5, 0x81, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0x9B };
static const symbol s_3_77[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0x9B };
static const symbol s_3_78[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0x9B };
static const symbol s_3_79[6] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x9B };
static const symbol s_3_80[6] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x9B };
static const symbol s_3_81[9] = { 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_3_82[12] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_3_83[9] = { 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_3_84[12] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_3_85[12] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0x8F, 0xE0, 0xA4, 0x95, 0xE0, 0xA4, 0xBE };
static const symbol s_3_86[6] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA4, 0xBE };
static const symbol s_3_87[9] = { 0xE0, 0xA4, 0x87, 0xE0, 0xA4, 0xA6, 0xE0, 0xA4, 0xBE };
static const symbol s_3_88[9] = { 0xE0, 0xA4, 0xBF, 0xE0, 0xA4, 0xA6, 0xE0, 0xA4, 0xBE };
static const symbol s_3_89[12] = { 0xE0, 0xA4, 0xA6, 0xE0, 0xA5, 0x87, 0xE0, 0xA4, 0x96, 0xE0, 0xA4, 0xBF };
static const symbol s_3_90[12] = { 0xE0, 0xA4, 0xAE, 0xE0, 0xA4, 0xBE, 0xE0, 0xA4, 0xA5, 0xE0, 0xA4, 0xBF };

static const struct among a_3[91] =
{
{ 9, s_3_0, -1, 1, 0},
{ 9, s_3_1, -1, 1, 0},
{ 12, s_3_2, 1, 1, 0},
{ 12, s_3_3, 1, 1, 0},
{ 12, s_3_4, -1, 1, 0},
{ 6, s_3_5, -1, 1, 0},
{ 6, s_3_6, -1, 1, 0},
{ 6, s_3_7, -1, 1, 0},
{ 9, s_3_8, 7, 1, 0},
{ 12, s_3_9, 8, 1, 0},
{ 9, s_3_10, 7, 1, 0},
{ 6, s_3_11, -1, 1, 0},
{ 9, s_3_12, -1, 1, 0},
{ 9, s_3_13, -1, 1, 0},
{ 6, s_3_14, -1, 1, 0},
{ 6, s_3_15, -1, 1, 0},
{ 6, s_3_16, -1, 1, 0},
{ 9, s_3_17, -1, 1, 0},
{ 12, s_3_18, 17, 1, 0},
{ 9, s_3_19, -1, 1, 0},
{ 6, s_3_20, -1, 1, 0},
{ 9, s_3_21, 20, 1, 0},
{ 9, s_3_22, 20, 1, 0},
{ 9, s_3_23, -1, 1, 0},
{ 12, s_3_24, 23, 1, 0},
{ 9, s_3_25, -1, 1, 0},
{ 12, s_3_26, 25, 1, 0},
{ 12, s_3_27, 25, 1, 0},
{ 6, s_3_28, -1, 1, 0},
{ 9, s_3_29, 28, 1, 0},
{ 9, s_3_30, 28, 1, 0},
{ 6, s_3_31, -1, 1, 0},
{ 9, s_3_32, 31, 1, 0},
{ 12, s_3_33, 31, 1, 0},
{ 9, s_3_34, 31, 1, 0},
{ 9, s_3_35, 31, 1, 0},
{ 12, s_3_36, 35, 1, 0},
{ 12, s_3_37, 35, 1, 0},
{ 6, s_3_38, -1, 1, 0},
{ 9, s_3_39, 38, 1, 0},
{ 9, s_3_40, 38, 1, 0},
{ 12, s_3_41, 40, 1, 0},
{ 9, s_3_42, 38, 1, 0},
{ 9, s_3_43, 38, 1, 0},
{ 6, s_3_44, -1, 1, 0},
{ 12, s_3_45, 44, 1, 0},
{ 12, s_3_46, 44, 1, 0},
{ 12, s_3_47, 44, 1, 0},
{ 9, s_3_48, -1, 1, 0},
{ 12, s_3_49, 48, 1, 0},
{ 12, s_3_50, 48, 1, 0},
{ 15, s_3_51, 50, 1, 0},
{ 12, s_3_52, 48, 1, 0},
{ 12, s_3_53, 48, 1, 0},
{ 12, s_3_54, -1, 1, 0},
{ 12, s_3_55, -1, 1, 0},
{ 12, s_3_56, -1, 1, 0},
{ 9, s_3_57, -1, 1, 0},
{ 9, s_3_58, -1, 1, 0},
{ 15, s_3_59, 58, 1, 0},
{ 12, s_3_60, -1, 1, 0},
{ 12, s_3_61, -1, 1, 0},
{ 9, s_3_62, -1, 1, 0},
{ 12, s_3_63, 62, 1, 0},
{ 12, s_3_64, 62, 1, 0},
{ 15, s_3_65, 64, 1, 0},
{ 12, s_3_66, 62, 1, 0},
{ 12, s_3_67, 62, 1, 0},
{ 9, s_3_68, -1, 1, 0},
{ 12, s_3_69, 68, 1, 0},
{ 9, s_3_70, -1, 1, 0},
{ 3, s_3_71, -1, 1, 0},
{ 6, s_3_72, 71, 1, 0},
{ 6, s_3_73, 71, 1, 0},
{ 9, s_3_74, 73, 1, 0},
{ 15, s_3_75, 74, 1, 0},
{ 15, s_3_76, 71, 1, 0},
{ 12, s_3_77, 71, 1, 0},
{ 12, s_3_78, 71, 1, 0},
{ 6, s_3_79, 71, 1, 0},
{ 6, s_3_80, 71, 1, 0},
{ 9, s_3_81, -1, 1, 0},
{ 12, s_3_82, 81, 1, 0},
{ 9, s_3_83, -1, 1, 0},
{ 12, s_3_84, 83, 1, 0},
{ 12, s_3_85, 83, 1, 0},
{ 6, s_3_86, -1, 1, 0},
{ 9, s_3_87, 86, 1, 0},
{ 9, s_3_88, 86, 1, 0},
{ 12, s_3_89, -1, 1, 0},
{ 12, s_3_90, -1, 1, 0}
};

static const symbol s_0[] = { 0xE0, 0xA4, 0x8F };
static const symbol s_1[] = { 0xE0, 0xA5, 0x87 };
static const symbol s_2[] = { 0xE0, 0xA4, 0xAF, 0xE0, 0xA5, 0x8C };
static const symbol s_3[] = { 0xE0, 0xA4, 0x9B, 0xE0, 0xA5, 0x8C };
static const symbol s_4[] = { 0xE0, 0xA4, 0xA8, 0xE0, 0xA5, 0x8C };
static const symbol s_5[] = { 0xE0, 0xA4, 0xA5, 0xE0, 0xA5, 0x87 };
static const symbol s_6[] = { 0xE0, 0xA4, 0xA4, 0xE0, 0xA5, 0x8D, 0xE0, 0xA4, 0xB0 };

static int r_remove_category_1(struct SN_env * z) {
    int among_var;
    z->ket = z->c;
    among_var = find_among_b(z, a_0, 17);
    if (!(among_var)) return 0;
    z->bra = z->c;
    switch (among_var) {
        case 1:
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            break;
        case 2:
            {   int m1 = z->l - z->c; (void)m1;
                {   int m2 = z->l - z->c; (void)m2;
                    if (!(eq_s_b(z, 3, s_0))) goto lab3;
                    goto lab2;
                lab3:
                    z->c = z->l - m2;
                    if (!(eq_s_b(z, 3, s_1))) goto lab1;
                }
            lab2:
                goto lab0;
            lab1:
                z->c = z->l - m1;
                {   int ret = slice_del(z);
                    if (ret < 0) return ret;
                }
            }
        lab0:
            break;
    }
    return 1;
}

static int r_check_category_2(struct SN_env * z) {
    z->ket = z->c;
    if (z->c - 2 <= z->lb || z->p[z->c - 1] >> 5 != 4 || !((262 >> (z->p[z->c - 1] & 0x1f)) & 1)) return 0;
    if (!(find_among_b(z, a_1, 3))) return 0;
    z->bra = z->c;
    return 1;
}

static int r_remove_category_2(struct SN_env * z) {
    int among_var;
    z->ket = z->c;
    if (z->c - 2 <= z->lb || z->p[z->c - 1] >> 5 != 4 || !((262 >> (z->p[z->c - 1] & 0x1f)) & 1)) return 0;
    among_var = find_among_b(z, a_2, 3);
    if (!(among_var)) return 0;
    z->bra = z->c;
    switch (among_var) {
        case 1:
            {   int m1 = z->l - z->c; (void)m1;
                if (!(eq_s_b(z, 6, s_2))) goto lab1;
                goto lab0;
            lab1:
                z->c = z->l - m1;
                if (!(eq_s_b(z, 6, s_3))) goto lab2;
                goto lab0;
            lab2:
                z->c = z->l - m1;
                if (!(eq_s_b(z, 6, s_4))) goto lab3;
                goto lab0;
            lab3:
                z->c = z->l - m1;
                if (!(eq_s_b(z, 6, s_5))) return 0;
            }
        lab0:
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            break;
        case 2:
            if (!(eq_s_b(z, 9, s_6))) return 0;
            {   int ret = slice_del(z);
                if (ret < 0) return ret;
            }
            break;
    }
    return 1;
}

static int r_remove_category_3(struct SN_env * z) {
    z->ket = z->c;
    if (!(find_among_b(z, a_3, 91))) return 0;
    z->bra = z->c;
    {   int ret = slice_del(z);
        if (ret < 0) return ret;
    }
    return 1;
}

extern int nepali_UTF_8_stem(struct SN_env * z) {
    z->lb = z->c; z->c = z->l;

    {   int m1 = z->l - z->c; (void)m1;
        {   int ret = r_remove_category_1(z);
            if (ret < 0) return ret;
        }
        z->c = z->l - m1;
    }
    {   int m2 = z->l - z->c; (void)m2;
        while(1) {
            int m3 = z->l - z->c; (void)m3;
            {   int m4 = z->l - z->c; (void)m4;
                {   int m5 = z->l - z->c; (void)m5;
                    {   int ret = r_check_category_2(z);
                        if (ret == 0) goto lab2;
                        if (ret < 0) return ret;
                    }
                    z->c = z->l - m5;
                    {   int ret = r_remove_category_2(z);
                        if (ret == 0) goto lab2;
                        if (ret < 0) return ret;
                    }
                }
            lab2:
                z->c = z->l - m4;
            }
            {   int ret = r_remove_category_3(z);
                if (ret == 0) goto lab1;
                if (ret < 0) return ret;
            }
            continue;
        lab1:
            z->c = z->l - m3;
            break;
        }
        z->c = z->l - m2;
    }
    z->c = z->lb;
    return 1;
}

extern struct SN_env * nepali_UTF_8_create_env(void) { return SN_create_env(0, 0); }

extern void nepali_UTF_8_close_env(struct SN_env * z) { SN_close_env(z, 0); }

