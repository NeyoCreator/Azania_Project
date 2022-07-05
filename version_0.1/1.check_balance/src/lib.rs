use scrypto::prelude::*;

blueprint! {
    struct UserVault {
        //0.DEFINE RESOURCE
        user_vault: Vault

    }

    impl UserVault {
        //1.INSTANTIATE
        pub fn instatiate_dnr() -> ComponentAddress{
            //1.1.CREATE TOKEN
            let my_bucket: Bucket = ResourceBuilder::new_fungible()
                .metadata("name", "DinarToken")
                .metadata("symbol", "DNR")
                .initial_supply(100);
            //1.2.INSTANTIATE AND POPULATING RESOURCE
            Self{
                user_vault: Vault::with_bucket(my_bucket)
            }.instantiate().globalize()
        
        }

        //2.MEHTOD
        pub fn check_balance(&mut self) -> Bucket{
            info!("My balance is: {}", self.user_vault.amount());
            self.user_vault.take(0)
        }


    }
}