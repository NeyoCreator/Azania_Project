use scrypto::prelude::*;

blueprint! {
    struct UserVault {
        user_vault : Vault
    }

    impl UserVault {
        pub fn instantiate_vault() -> (ComponentAddress, Bucket){
            //1. ADMIN BADGE
            let admin_badge : Bucket = ResourceBuilder::new_fungible()
                        .divisibility(DIVISIBILITY_NONE)
                        .metadata("name", "admin_badge")
                        .initial_supply(1);

            //2. ACCESS RULES
            let access_rules = AccessRules::new()
            .method("withdraw", rule!(require(admin_badge.resource_address()))) 
            .default(rule!(allow_all));

        (Self {user_vault: Vault::new(RADIX_TOKEN)}.instantiate().add_access_check(access_rules).globalize(),admin_badge)
            
        }

        pub fn withdraw(&mut self){
            //3. CALL METHOD 
            self.user_vault.take(4);
        }
    }
    
}