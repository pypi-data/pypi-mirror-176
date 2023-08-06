#ifndef	tajk_data_h
#define tajk_data_h

#ifdef __cplusplus
extern "C"  {
#endif

struct stru_tajk_field	{	//�ֶ������ֵ��
	int ver;	//�汾��Ŀǰ֧��2.1��2.2����ӦȡֵΪ21��22��Ϊ0��ʾ�������
	int id;		//�ֶ�ԭʼid
	char name[50],type;		//�ֶ��������ͣ�C��A��N��
	int size,decpos;		//��С��С��λ��
	char desc[1500];			//����
};

struct stru_tajk_datafile_field{//���ӿ��ļ��ֶ��б�
	int ver;	//�汾��Ŀǰ֧��2.1��2.2����ӦȡֵΪ21��22��Ϊ0��ʾ�������
	char filemode[3];//�ļ�����,��01,02����
	int tfid;	//�ֶ�id��ע�������id���ǽӿ����ԭʼid������tajk_field�ж�Ӧ�����
};

extern struct stru_tajk_field tajk_field[];	//ȫ���ֶ������ֵ��
extern struct stru_tajk_datafile_field tajk_datafile_field[];//�����ļ����ֶζ�Ӧ��ϵ

#ifdef __cplusplus
}
#endif

#endif
